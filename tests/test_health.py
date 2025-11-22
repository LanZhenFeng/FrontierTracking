import pytest
import httpx
from httpx import AsyncClient

# 测试基础 URL
BASE_URL = "http://localhost:8000"


@pytest.mark.asyncio
async def test_health_check():
    """测试健康检查端点"""
    async with AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


# 同步版本（如果需要）
def test_health_check_sync():
    """同步测试健康检查端点"""
    with httpx.Client(base_url=BASE_URL) as client:
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


# 直接运行脚本
if __name__ == "__main__":
    import asyncio
    
    async def check_health():
        async with AsyncClient(base_url=BASE_URL) as client:
            try:
                response = await client.get("/health", timeout=5.0)
                print(f"Status Code: {response.status_code}")
                print(f"Response: {response.json()}")
            except httpx.ConnectError:
                print(f"❌ 无法连接到 {BASE_URL}")
            except Exception as e:
                print(f"❌ 错误: {e}")
    
    asyncio.run(check_health())