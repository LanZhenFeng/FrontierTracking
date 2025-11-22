import logging
import sys
from pathlib import Path
from typing import Optional
from rich.console import Console
from rich.logging import RichHandler
from rich.theme import Theme
from rich.traceback import install as install_rich_traceback

# 安装 rich traceback
install_rich_traceback(show_locals=True)

# 定义自定义主题
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "bold red",
    "critical": "bold white on red",
    "debug": "dim blue",
    "logging.level.info": "cyan",
    "logging.level.warning": "yellow",
    "logging.level.error": "bold red",
    "logging.level.critical": "bold white on red",
    "logging.level.debug": "dim blue",
})

class LoggerSetup:
    """日志系统配置"""
    
    _loggers = {}
    
    @classmethod
    def get_logger(
        cls,
        name: str,
        level: str = "INFO",
        log_file: Optional[Path] = None,
        enable_rich: bool = True
    ) -> logging.Logger:
        """
        获取配置好的 logger
        
        Args:
            name: logger 名称
            level: 日志级别 (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            log_file: 日志文件路径
            enable_rich: 是否启用 rich 格式化
            
        Returns:
            配置好的 logger 实例
        """
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        logger.handlers.clear()
        
        # Rich Console Handler
        if enable_rich:
            console = Console(stderr=True)
            rich_handler = RichHandler(
                console=console,
                show_time=True,
                show_path=True,
                markup=True,
                rich_tracebacks=True,
                tracebacks_show_locals=True,
                omit_repeated_times=False,
                log_time_format="[%H:%M:%S]"
            )
            rich_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter("%(message)s")
            rich_handler.setFormatter(formatter)
            logger.addHandler(rich_handler)
        else:
            # 标准 StreamHandler
            stream_handler = logging.StreamHandler(sys.stdout)
            stream_handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)
        
        # 文件 Handler
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        # 防止日志传播到根 logger
        logger.propagate = False
        
        cls._loggers[name] = logger
        return logger


# 默认 logger 实例
def get_logger(
    name: str = "frontiertracker",
    level: str = "INFO",
    log_file: Optional[Path] = None
) -> logging.Logger:
    """
    快捷方法获取 logger
    
    Example:
        >>> from frontiertracker.utils.logging import get_logger
        >>> logger = get_logger(__name__)
        >>> logger.info("Hello World")
        >>> logger.warning("This is a warning")
        >>> logger.error("This is an error")
    """
    return LoggerSetup.get_logger(name, level, log_file)


# 项目根目录日志
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
LOG_DIR = PROJECT_ROOT / "logs"

# 默认日志文件
DEFAULT_LOG_FILE = LOG_DIR / "app.log"

# 创建默认 logger
logger = get_logger(
    name="frontiertracker",
    level="INFO",
    log_file=DEFAULT_LOG_FILE
)


# 便捷函数
def debug(msg: str, **kwargs):
    """输出 DEBUG 日志"""
    logger.debug(msg, **kwargs)


def info(msg: str, **kwargs):
    """输出 INFO 日志"""
    logger.info(msg, **kwargs)


def warning(msg: str, **kwargs):
    """输出 WARNING 日志"""
    logger.warning(msg, **kwargs)


def error(msg: str, **kwargs):
    """输出 ERROR 日志"""
    logger.error(msg, **kwargs)


def critical(msg: str, **kwargs):
    """输出 CRITICAL 日志"""
    logger.critical(msg, **kwargs)


def exception(msg: str, **kwargs):
    """输出异常日志（包含 traceback）"""
    logger.exception(msg, **kwargs)