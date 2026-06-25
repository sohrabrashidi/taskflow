from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime
from bson import ObjectId
from app.models import TaskCreate, TaskUpdate, TaskOut
from app.database import get_db
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=list[TaskOut])
async def list_tasks(
    status: str = Query(None),
    priority: str = Query(None),
    skip: int = 0,
    limit: int = 20,
    user_id: str = Depends(get_current_user),
):
    db = get_db()
    query = {"user_id": user_id}
    if status:
        query["status"] = status
    if priority:
        query["priority"] = priority
    cursor = db.tasks.find(query).skip(skip).limit(limit).sort("created_at", -1)
    tasks = []
    async for doc in cursor:
        doc["id"] = str(doc.pop("_id"))
        tasks.append(TaskOut(**doc))
    return tasks


@router.post("", response_model=TaskOut, status_code=201)
async def create_task(task: TaskCreate, user_id: str = Depends(get_current_user)):
    db = get_db()
    doc = task.model_dump()
    doc["user_id"] = user_id
    doc["created_at"] = datetime.utcnow()
    result = await db.tasks.insert_one(doc)
    doc["id"] = str(result.inserted_id)
    return TaskOut(**doc)


@router.get("/{task_id}", response_model=TaskOut)
async def get_task(task_id: str, user_id: str = Depends(get_current_user)):
    db = get_db()
    doc = await db.tasks.find_one({"_id": ObjectId(task_id), "user_id": user_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Task not found")
    doc["id"] = str(doc.pop("_id"))
    return TaskOut(**doc)


@router.put("/{task_id}", response_model=TaskOut)
async def update_task(task_id: str, update: TaskUpdate, user_id: str = Depends(get_current_user)):
    db = get_db()
    changes = {k: v for k, v in update.model_dump().items() if v is not None}
    if not changes:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await db.tasks.find_one_and_update(
        {"_id": ObjectId(task_id), "user_id": user_id},
        {"$set": changes},
        return_document=True,
    )
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    result["id"] = str(result.pop("_id"))
    return TaskOut(**result)


@router.delete("/{task_id}", status_code=204)
async def delete_task(task_id: str, user_id: str = Depends(get_current_user)):
    db = get_db()
    result = await db.tasks.delete_one({"_id": ObjectId(task_id), "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Task not found")
