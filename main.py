from datetime import datetime
from random import randint
from fastapi import FastAPI, HTTPException, Request, Response
from typing import Any

from httpx import request


App = FastAPI(root_path="/Api/V1")


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


@App.get("/campaigns")
async def read_campaigns():
    return {"message": data}


@App.get("/campaigns/{id}")
async def read_campaign(id: int):
    for campaign in data:
        if campaign.get("campaign_id") == id:
            return {"campaign": campaign}
    raise HTTPException(status_code=404)


@App.post("/campaigns", status_code=201)
async def create_campaign(body: dict[str, Any]):
    new: Any = {
        "campaign_id": randint(100, 1000),
        "name": body.get("name"),
        "due_date": body.get("due_date"),
        "created_at": datetime.now()
    }
    data.append(new)
    return {"campaign": new}


@App.put("/campaigns/{id}")
async def update_campaign(id: int, body: dict[str, Any]):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            update: Any = {
                "campaign_id": id,
                "name": body.get("name"),
                "due_date": body.get("due_date"),
                "created_at": campaign.get("created_at")
            }
            data[index] = update
            return {"campaign": update}
    raise HTTPException(status_code=404)


@App.delete("/campaigns/{id}")
async def delete_campaign(id: int):
    for index, campaign in enumerate(data):
        if campaign.get("campaign_id") == id:
            data.pop(index)
            return Response(status_code=204)
    raise HTTPException(status_code=404)
