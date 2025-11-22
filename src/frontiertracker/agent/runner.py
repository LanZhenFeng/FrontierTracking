# src/projectname/agent_runner/runner.py

import time
from sqlalchemy.orm import Session
from src.frontiertracker.db.database import SessionLocal
from src.frontiertracker.db.models import Task, TaskStatus

def run_agent_task(task_id: int):
    """
    实际的 Agent 任务执行函数
    可以调用 LangChain/LangGraph 等框架进行智能处理
    """
    db: Session = SessionLocal()
    task = None
    try:
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return

        # 更新状态为 running
        task.status = TaskStatus.RUNNING
        db.commit()

        # TODO: 在这里集成实际的 Agent 逻辑
        # 例如：调用 LangChain、搜索 arXiv、处理数据等
        time.sleep(3)  # 暂时用 sleep 模拟

        # 更新结果
        task.status = TaskStatus.COMPLETED
        task.result_summary = f"Agent processed query: {task.query}"
        task.result_details = f"Sources: {task.sources}, Format: {task.output_format}"
        db.commit()
    except Exception as e:
        # 处理错误
        task.status = TaskStatus.FAILED
        task.result_summary = f"Error: {str(e)}"
        db.commit()
    finally:
        db.close()
