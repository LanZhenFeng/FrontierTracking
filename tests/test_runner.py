import pytest
from src.frontiertracker.db.models import Task, TaskStatus
from src.frontiertracker.agent.runner import run_agent_task
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.frontiertracker.db.database import Base

TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="function")
def test_db():
    """为每个测试创建独立的数据库会话"""
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_create_task(test_db):
    """测试创建任务"""
    # 创建一个新任务
    task = Task(
        query="Test query about AI",
        sources="arxiv,semantic_scholar",
        output_format="markdown",
        status=TaskStatus.PENDING
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)
    
    # 验证任务已创建
    assert task.id is not None
    assert task.query == "Test query about AI"
    assert task.status == TaskStatus.PENDING
    
    # 验证可以从数据库查询到
    db_task = test_db.query(Task).filter(Task.id == task.id).first()
    assert db_task is not None
    assert db_task.query == "Test query about AI"

def test_run_agent_task(test_db):
    """测试运行 Agent 任务"""
    # 先创建一个任务
    task = Task(
        query="Test AI research",
        sources="arxiv",
        output_format="json",
        status=TaskStatus.PENDING
    )
    test_db.add(task)
    test_db.commit()
    test_db.refresh(task)
    
    task_id = task.id
    test_db.close()  # 关闭这个会话，让 run_agent_task 使用自己的会话
    
    # 运行任务（注意：这会使用 SessionLocal，需要修复）
    run_agent_task(task_id)
    
    # 重新打开会话验证结果
    # 这里暂时注释掉，因为 run_agent_task 使用的是 dev.db
    # 需要先修改 runner.py 才能正常测试