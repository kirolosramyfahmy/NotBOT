from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.db.session import get_db
from app.models.mission import Mission
from app.schemas.mission import MissionCreate, MissionResponse
from app.services.crawler import run_crawler_task

router = APIRouter()

@router.post("/missions/", response_model=MissionResponse, status_code=status.HTTP_202_ACCEPTED)
async def create_mission(
    mission_in: MissionCreate, 
    background_tasks: BackgroundTasks, 
    db: AsyncSession = Depends(get_db)
):
    mission = Mission(
        brand_name=mission_in.brand_name,
        target_url=str(mission_in.target_url)
    )
    db.add(mission)
    await db.commit()
    await db.refresh(mission)
    
    background_tasks.add_task(run_crawler_task, mission.id)
    
    return mission

@router.get("/missions/", response_model=List[MissionResponse])
async def list_missions(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    query = select(Mission).order_by(Mission.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    missions = result.scalars().all()
    return missions

@router.get("/missions/{mission_id}", response_model=MissionResponse)
async def get_mission(mission_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Mission).where(Mission.id == mission_id)
    result = await db.execute(query)
    mission = result.scalar_one_or_none()
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")
    return mission
