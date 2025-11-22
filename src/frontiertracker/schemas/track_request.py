from pydantic import BaseModel, Field
from typing import List, Optional

class TrackRequest(BaseModel):
    query: str = Field(..., description="要追踪的关键词或主题")
    sources: List[str] = Field(..., description="要检索的文献／数据源清单，比如 ['arxiv','pubmed']")
    output_format: Optional[str] = Field("summary", description="输出格式，可选：summary / detailed")

class TrackResponse(BaseModel):
    task_id: int = Field(..., description="创建任务后返回的任务ID")

class TrackResultResponse(BaseModel):
    task_id: int = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态，例如 PENDING, RUNNING, COMPLETED, FAILED")
    result_summary: Optional[str] = Field(None, description="如果完成，则返回摘要结果")
    result_details: Optional[str] = Field(None, description="如果请求 “detailed” 格式，可返回更详报告")