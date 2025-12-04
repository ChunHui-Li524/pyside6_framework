"""
初始化脚本
用于首次运行应用程序时创建必要的目录结构和配置文件
"""

import os
import sys
import json
from core.log_manager import LogManager
from utils.config_manager import ConfigManager
from utils.file_utils import FileUtils


def initialize_app():
    """初始化应用程序环境
    
    创建必要的目录结构和默认配置文件
    """
    print("正在初始化应用程序环境...")
    
    try:
        # 初始化日志管理器
        logger = LogManager()
        logger.info("开始应用程序初始化")
        
        # 初始化配置管理器
        config_manager = ConfigManager()
        
        # 初始化文件工具
        file_utils = FileUtils()
        
        # 获取配置目录
        config_dir = config_manager.get_config_dir()
        logger.info(f"配置目录: {config_dir}")
        
        # 创建配置目录
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
            logger.info(f"已创建配置目录: {config_dir}")
        else:
            logger.info("配置目录已存在")
        
        # 获取配置文件路径
        config_path = config_manager.get_config_path()
        logger.info(f"配置文件路径: {config_path}")
        
        # 如果配置文件不存在，创建默认配置
        if not os.path.exists(config_path):
            # 创建默认配置
            default_config = {
                "application": {
                    "name": "PySide6 Framework",
                    "version": "1.0.0",
                    "debug_mode": True,
                    "theme": "light",
                    "language": "zh_CN",
                    "window_size": [1024, 768],
                    "window_position": [100, 100],
                    "auto_save": True
                },
                "logging": {
                    "level": "INFO",
                    "file_logging": True,
                    "log_file": os.path.join(config_dir, "app.log"),
                    "max_bytes": 5242880,  # 5MB
                    "backup_count": 5
                },
                "services": {
                    "example_service": {
                        "enabled": True,
                        "cache_timeout": 300  # 5分钟
                    }
                },
                "ui": {
                    "font_family": "SimHei",
                    "font_size": 10,
                    "show_toolbar": True,
                    "show_statusbar": True,
                    "animation_enabled": True
                }
            }
            
            # 保存默认配置
            file_utils.write_json_file(config_path, default_config)
            logger.info(f"已创建默认配置文件: {config_path}")
            print(f"已创建默认配置文件: {config_path}")
        else:
            logger.info("配置文件已存在")
            print("配置文件已存在")
        
        # 创建日志目录
        log_dir = os.path.join(config_dir, "logs")
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            logger.info(f"已创建日志目录: {log_dir}")
        else:
            logger.info("日志目录已存在")
        
        # 创建数据目录
        data_dir = os.path.join(config_dir, "data")
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"已创建数据目录: {data_dir}")
        else:
            logger.info("数据目录已存在")
        
        # 初始化完成
        logger.info("应用程序初始化完成")
        print("应用程序初始化完成!")
        print("\n可以运行 main.py 启动应用程序")
        
        return True
        
    except Exception as e:
        print(f"初始化失败: {str(e)}")
        # 尝试记录到文件
        try:
            error_log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "init_error.log")
            with open(error_log_path, "w", encoding="utf-8") as f:
                f.write(f"初始化失败: {str(e)}\n")
                import traceback
                f.write(traceback.format_exc())
            print(f"错误详情已记录到: {error_log_path}")
        except:
            pass
        return False


def main():
    """主函数"""
    success = initialize_app()
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
