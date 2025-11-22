from typing import Optional
from sqlalchemy.orm import Session

from src.frontiertracker.db.models import Task, TaskStatus
from src.frontiertracker.schemas.track_request import TrackRequest

def create_task_service(db: Session, req: TrackRequest) -> Task:
    """
    创建新任务：
    - 将 Pydantic 请求对象转换为 DB 模型 Task
    - 状态设为 pending
    - 插入数据库、刷新、返回 Task 实例
    """
    # 将 sources 列表转换为字符串存储，例如 "arxiv,pubmed"
    sources_str = ",".join(req.sources)
    task = Task(
        query=req.query,
        source=sources_str,
        output_format=req.output_format,
        status=TaskStatus.PENDING
    )
    db.add(task)
    db.commit()
    db.refresh(task)  # 刷新以获得 auto-generated fields（如 id）
    return task

def get_task_service(db: Session, task_id: int) -> Optional[Task]:
    """
    根据 task_id 获取任务记录
    """
    return db.query(Task).filter(Task.id == task_id).first()
