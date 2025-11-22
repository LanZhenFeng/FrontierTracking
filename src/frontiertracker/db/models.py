
import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, func
from src.frontiertracker.db.database import Base

class TaskStatus(enum.Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, nullable=False, comment="用户提交的关键词查询")
    sources = Column(Text, nullable=False, comment="数据来源，例如 arxiv，pubmed，以逗号分隔或 JSON ")
    output_format = Column(String, nullable=False, default="summary", comment="用户要求的输出格式")
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False, comment="任务状态")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="任务创建时间")
    completed_at = Column(DateTime(timezone=True), nullable=True, comment="任务完成时间，可能为空")
    result_summary = Column(Text, nullable=True, comment="任务结果的摘要")
    result_details = Column(Text, nullable=True, comment="任务结果的详细信息")

    def __repr__(self):
        return f"<Task(id={self.id}, query='{self.query}', status='{self.status.value}')>"