from datetime import datetime, timezone
from fastapi.concurrency import asynccontextmanager
from pydantic import BaseModel
from typing_extensions import Annotated
from fastapi import FastAPI, HTTPException, Response
from typing import Any, Generic, TypeVar
from fastapi.params import Depends
from sqlmodel import SQLModel, Field, Session, create_engine, select


class Campaign(SQLModel, table=True):
    campaign_id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    due_date: datetime | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(
        timezone.utc), nullable=True, index=True)


class CampaignCreate(SQLModel):
    name: str
    due_date: datetime | None = None


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connection_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connection_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        if not session.exec(select(Campaign)).first():
            session.add_all([
                Campaign(name="summer launch",
                         due_date=datetime.now(timezone.utc)),
                Campaign(name="Campaign 2", due_date=datetime(
                    2024, 7, 15, tzinfo=timezone.utc)),
                Campaign(name="Campaign 3", due_date=datetime(
                    2024, 8, 20, tzinfo=timezone.utc))
            ])
            session.commit()
    yield


App = FastAPI(root_path="/Api/V1", lifespan=lifespan)


@App.get("/")
async def root():
    return {"message": "hello World"}

data: Any = [
    {
        "campaign_id": 1,
        "name": "summer launch",
        "due_date": datetime.now(),
        "created_at": "2024-06-01"
    },
    {
        "campaign_id": 2,
        "name": "Campaign 2",
        "due_date": "2024-07-15",
        "created_at": "2024-06-05"
    },
    {
        "campaign_id": 3,
        "name": "Campaign 3",
        "due_date": "2024-08-20",
        "created_at": "2024-06-10"
    }
]

"""
campaigns
-campaign_id
-name
-due_date
-created_at
"""

T = TypeVar("T")


class Response(BaseModel, Generic[T]):
    data: T


@App.get("/campaigns", response_model=Response[list[Campaign]])
async def read_campaigns(session: SessionDep):
    data = session.exec(select(Campaign)).all()
    return {"data": data}


@App.get("/campaigns/{id}", response_model=Response[Campaign])
async def read_campaign(id: int, session: SessionDep):
    data = session.get(Campaign, id)
    if not data:
        raise HTTPException(status_code=404)
    return {"data": data}


@App.post("/campaigns", status_code=201, response_model=Response[Campaign])
async def create_campaign(body: CampaignCreate, session: SessionDep):
    db_campaign = Campaign.model_validate(body)

    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data": db_campaign}


@App.put("/campaigns/{id}", response_model=Response[Campaign])
async def update_campaign(id: int, body: CampaignCreate, session: SessionDep):
    db_campaign = session.get(Campaign, id)
    if not db_campaign:
        raise HTTPException(status_code=404)

    db_campaign.name = body.name
    db_campaign.due_date = body.due_date

    session.add(db_campaign)
    session.commit()
    session.refresh(db_campaign)
    return {"data": db_campaign}

@App.delete("/campaigns/{id}", status_code=204)
async def delete_campaign(id: int, session: SessionDep):
    db_campaign = session.get(Campaign, id)
    if not db_campaign:
        raise HTTPException(status_code=404)

    session.delete(db_campaign)
    session.commit()


# @App.get("/campaigns")
# async def read_campaigns():
#     return {"message": data}


# @App.get("/campaigns/{id}")
# async def read_campaign(id: int):
#     for campaign in data:
#         if campaign.get("campaign_id") == id:
#             return {"campaign": campaign}
#     raise HTTPException(status_code=404)


# @App.post("/campaigns", status_code=201)
# async def create_campaign(body: dict[str, Any]):
#     new: Any = {
#         "campaign_id": randint(100, 1000),
#         "name": body.get("name"),
#         "due_date": body.get("due_date"),
#         "created_at": datetime.now()
#     }
#     data.append(new)
#     return {"campaign": new}


# @App.put("/campaigns/{id}")
# async def update_campaign(id: int, body: dict[str, Any]):
#     for index, campaign in enumerate(data):
#         if campaign.get("campaign_id") == id:
#             update: Any = {
#                 "campaign_id": id,
#                 "name": body.get("name"),
#                 "due_date": body.get("due_date"),
#                 "created_at": campaign.get("created_at")
#             }
#             data[index] = update
#             return {"campaign": update}
#     raise HTTPException(status_code=404)


# @App.delete("/campaigns/{id}")
# async def delete_campaign(id: int):
#     for index, campaign in enumerate(data):
#         if campaign.get("campaign_id") == id:
#             data.pop(index)
#             return Response(status_code=204)
#     raise HTTPException(status_code=404)
