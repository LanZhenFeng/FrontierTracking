from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from src.frontiertracker.schemas.track_request import TrackRequest, TrackResponse, TrackResultResponse
from src.frontiertracker.db.database import get_db
from src.frontiertracker.services.task_service import create_task_service, get_task_service
from src.frontiertracker.agent.runner import run_agent_task  # 假定你后续有这个模块
from src.frontiertracker.utils.logger import logger

router = APIRouter(prefix="/api/v1", tags=["Frontier Tracker"])

@router.post("/track-request", response_model=TrackResponse)
async def track_request(request: TrackRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """
    创建一个新的追踪任务：
    - 接收关键词、数据源、输出格式
    - 在数据库中插入一条任务（初始状态 pending）
    - 启动后台任务以异步执行 Agent（mock 或真实）
    - 返回 task_id 给客户端
    """
    task = create_task_service(db, request)
    # 将后台工作交给 agent_runner
    background_tasks.add_task(run_agent_task, task.id, db)
    return TrackResponse(task_id=task.id)

@router.get("/track-result/{task_id}", response_model=TrackResultResponse)
def track_result(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    查询任务状态或结果：
    - 从 DB 根据 task_id 查询任务
    - 如果不存在，返回 404
    - 若存在，返回 task_id, 状态, 如果完成则返回摘要／详情
    """
    task = get_task_service(db, task_id)
    if not task:
        logger.warning(f"任务ID {task_id} 未找到")
        raise HTTPException(status_code=404, detail="任务未找到")
    return TrackResultResponse(
        task_id=task.id,
        status=task.status.value,
        result_summary=task.result_summary,
        result_details=task.result_details
    )