import sys
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))

from src.frontiertracker.db.database import Base
from src.frontiertracker.main import app

# 使用独立的测试数据库
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
        # 清理测试数据
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    """FastAPI 测试客户端"""
    return TestClient(app)