"""
Logger 系统测试文件
测试所有日志功能和配置选项
"""
import sys
import pytest
import logging
from pathlib import Path
import tempfile
import shutil

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

from frontiertracker.utils.logger import (
    get_logger,
    logger as default_logger,
    debug,
    info,
    warning,
    error,
    critical,
    exception,
    LoggerSetup
)


class TestLoggerSetup:
    """测试 LoggerSetup 类"""
    
    def test_get_default_logger(self):
        """测试获取默认 logger"""
        logger = get_logger("test_default")
        assert logger is not None
        assert logger.name == "test_default"
        assert logger.level == logging.INFO
    
    def test_get_logger_with_custom_level(self):
        """测试自定义日志级别"""
        logger = get_logger("test_debug", level="DEBUG")
        assert logger.level == logging.DEBUG
        
        logger = get_logger("test_error", level="ERROR")
        assert logger.level == logging.ERROR
    
    def test_logger_singleton(self):
        """测试 logger 单例模式"""
        logger1 = get_logger("test_singleton")
        logger2 = get_logger("test_singleton")
        assert logger1 is logger2
    
    def test_logger_with_file_handler(self, tmp_path):
        """测试文件日志处理器"""
        log_file = tmp_path / "test.log"
        logger = get_logger("test_file", log_file=log_file)
        
        logger.info("Test message")
        
        assert log_file.exists()
        content = log_file.read_text()
        assert "Test message" in content
    
    def test_logger_propagation(self):
        """测试日志不传播到根 logger"""
        logger = get_logger("test_propagate")
        assert logger.propagate is False


class TestDefaultLogger:
    """测试默认 logger 实例"""
    
    def test_default_logger_exists(self):
        """测试默认 logger 是否存在"""
        assert default_logger is not None
        assert default_logger.name == "frontiertracker"
    
    def test_default_logger_methods(self):
        """测试默认 logger 的各种方法"""
        # 这些不应该抛出异常
        default_logger.debug("Debug message")
        default_logger.info("Info message")
        default_logger.warning("Warning message")
        default_logger.error("Error message")
        default_logger.critical("Critical message")


class TestConvenienceFunctions:
    """测试便捷函数"""
    
    def test_debug_function(self):
        """测试 debug 便捷函数"""
        try:
            debug("This is a debug message")
        except Exception as e:
            pytest.fail(f"debug() raised {e}")
    
    def test_info_function(self):
        """测试 info 便捷函数"""
        try:
            info("This is an info message")
        except Exception as e:
            pytest.fail(f"info() raised {e}")
    
    def test_warning_function(self):
        """测试 warning 便捷函数"""
        try:
            warning("This is a warning message")
        except Exception as e:
            pytest.fail(f"warning() raised {e}")
    
    def test_error_function(self):
        """测试 error 便捷函数"""
        try:
            error("This is an error message")
        except Exception as e:
            pytest.fail(f"error() raised {e}")
    
    def test_critical_function(self):
        """测试 critical 便捷函数"""
        try:
            critical("This is a critical message")
        except Exception as e:
            pytest.fail(f"critical() raised {e}")
    
    def test_exception_function(self):
        """测试 exception 便捷函数"""
        try:
            raise ValueError("Test exception")
        except ValueError:
            try:
                exception("An exception occurred")
            except Exception as e:
                pytest.fail(f"exception() raised {e}")


class TestLoggerFeatures:
    """测试日志系统特性"""
    
    def test_rich_markup(self):
        """测试 Rich markup 支持"""
        logger = get_logger("test_markup")
        
        # 这些不应该抛出异常
        logger.info("This is [bold]bold[/] text")
        logger.info("This is [red]red[/] text")
        logger.info("This is [bold yellow]bold yellow[/] text")
    
    def test_multiple_loggers(self):
        """测试创建多个不同的 logger"""
        logger1 = get_logger("module1", level="DEBUG")
        logger2 = get_logger("module2", level="INFO")
        logger3 = get_logger("module3", level="ERROR")
        
        assert logger1 is not logger2
        assert logger2 is not logger3
        assert logger1.level == logging.DEBUG
        assert logger2.level == logging.INFO
        assert logger3.level == logging.ERROR
    
    def test_logger_with_multiple_handlers(self, tmp_path):
        """测试 logger 同时输出到控制台和文件"""
        log_file = tmp_path / "multi.log"
        logger = get_logger("test_multi", log_file=log_file)
        
        test_message = "Test message for multiple handlers"
        logger.info(test_message)
        
        # 验证文件中有日志
        assert log_file.exists()
        content = log_file.read_text()
        assert test_message in content
    
    def test_exception_logging_with_traceback(self, tmp_path):
        """测试异常日志包含 traceback"""
        log_file = tmp_path / "exception.log"
        logger = get_logger("test_exception", log_file=log_file)
        
        try:
            result = 1 / 0
        except ZeroDivisionError:
            logger.exception("Division by zero occurred")
        
        # 验证文件中有 traceback 信息
        content = log_file.read_text()
        assert "Division by zero occurred" in content
        assert "ZeroDivisionError" in content


class TestLoggerIntegration:
    """集成测试"""
    
    def test_real_world_scenario(self, tmp_path):
        """测试真实使用场景"""
        log_file = tmp_path / "app.log"
        app_logger = get_logger("my_app", level="DEBUG", log_file=log_file)
        
        # 模拟应用启动
        app_logger.info("🚀 Application starting...")
        app_logger.debug("Loading configuration...")
        app_logger.info("✅ Configuration loaded")
        
        # 模拟处理请求
        app_logger.info("Processing request from user: [bold]john@example.com[/]")
        
        # 模拟警告
        app_logger.warning("⚠️  Cache miss for key: user_123")
        
        # 模拟错误
        try:
            raise ValueError("Invalid user input")
        except ValueError:
            app_logger.exception("❌ Error processing request")
        
        # 验证日志文件
        assert log_file.exists()
        content = log_file.read_text()
        assert "Application starting" in content
        assert "Loading configuration" in content
        assert "Cache miss" in content
        assert "ValueError" in content
    
    def test_module_specific_loggers(self):
        """测试为不同模块创建专用 logger"""
        db_logger = get_logger("frontiertracker.db", level="DEBUG")
        api_logger = get_logger("frontiertracker.api", level="INFO")
        
        db_logger.debug("Database query executed")
        api_logger.info("API request received")
        
        # 验证它们是不同的实例
        assert db_logger is not api_logger
        assert db_logger.name == "frontiertracker.db"
        assert api_logger.name == "frontiertracker.api"


# 直接运行测试
if __name__ == "__main__":
    print("=" * 60)
    print("Testing Logger System")
    print("=" * 60)
    
    # 测试 1: 基本日志输出
    print("\n1️⃣  Testing basic logging...")
    logger = get_logger("demo", level="DEBUG")
    logger.debug("🐛 This is a debug message")
    logger.info("ℹ️  This is an info message")
    logger.warning("⚠️  This is a [bold yellow]warning[/] message")
    logger.error("❌ This is an [bold red]error[/] message")
    logger.critical("🔥 This is a [bold red on white]critical[/] message")
    
    # 测试 2: 便捷函数
    print("\n2️⃣  Testing convenience functions...")
    info("Using convenience function")
    warning("This is easier to use")
    
    # 测试 3: 异常日志
    print("\n3️⃣  Testing exception logging...")
    try:
        result = 10 / 0
    except ZeroDivisionError:
        logger.exception("Caught an exception")
    
    # 测试 4: 文件日志
    print("\n4️⃣  Testing file logging...")
    temp_dir = Path(tempfile.mkdtemp())
    file_logger = get_logger(
        "file_test",
        level="DEBUG",
        log_file=temp_dir / "test.log"
    )
    file_logger.info("This will be written to file")
    print(f"📁 Log file created at: {temp_dir / 'test.log'}")
    
    # 测试 5: Rich 格式化
    print("\n5️⃣  Testing Rich formatting...")
    logger.info("This is [bold]bold[/]")
    logger.info("This is [italic]italic[/]")
    logger.info("This is [underline]underlined[/]")
    logger.info("This is [red]red[/] and [green]green[/] and [blue]blue[/]")
    logger.info("This is [bold yellow on blue]fancy[/]")
    
    print("\n" + "=" * 60)
    print("✅ All manual tests completed!")
    print("=" * 60)
    
    # 清理临时文件
    shutil.rmtree(temp_dir)