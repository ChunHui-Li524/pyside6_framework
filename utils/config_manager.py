import json
import os
from core.log_manager import LogManager
from utils.singleton import SingletonBase

class ConfigManager(SingletonBase):
    """
    配置管理器，用于处理应用程序配置的读取和保存
    支持JSON格式的配置文件操作
    """
    
    def __init__(self):
        """初始化配置管理器"""
        if hasattr(self, 'initialized'):
            return
            
        self.logger = LogManager()
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'config')
        self.config_file = os.path.join(self.config_dir, 'app_config.json')
        self.config_data = {}
        
        # 创建配置目录
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir)
            self.logger.info(f"创建配置目录: {self.config_dir}")
        
        # 加载配置文件
        self.load_config()
        self.initialized = True
    
    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                self.logger.info(f"配置文件加载成功: {self.config_file}")
            else:
                self.logger.info(f"配置文件不存在，将使用默认配置: {self.config_file}")
                # 创建默认配置
                self._create_default_config()
        except json.JSONDecodeError as e:
            self.logger.error(f"配置文件格式错误: {str(e)}")
            # 重新创建默认配置
            self._create_default_config()
        except Exception as e:
            self.logger.error(f"加载配置文件时出错: {str(e)}")
    
    def _create_default_config(self):
        """创建默认配置"""
        self.config_data = {
            'app': {
                'name': 'PySide6 Framework',
                'version': '1.0.0',
                'debug': True
            },
            'logging': {
                'level': 'INFO',
                'console_level': 'INFO',
                'file_level': 'DEBUG',
                'log_dir': 'logs'
            },
            'ui': {
                'theme': 'light',
                'font_size': 12,
                'window_position': {'x': 100, 'y': 100},
                'window_size': {'width': 800, 'height': 600}
            }
        }
        self.save_config()
    
    def save_config(self):
        """保存配置到文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"配置文件保存成功: {self.config_file}")
            return True
        except Exception as e:
            self.logger.error(f"保存配置文件时出错: {str(e)}")
            return False
    
    def get(self, key_path, default=None):
        """获取配置值
        
        Args:
            key_path: 配置键路径，支持嵌套键，如 'app.name'
            default: 默认值，当键不存在时返回
            
        Returns:
            配置值或默认值
        """
        keys = key_path.split('.')
        value = self.config_data
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            self.logger.warning(f"配置项不存在: {key_path}, 返回默认值: {default}")
            return default
    
    def set(self, key_path, value):
        """设置配置值
        
        Args:
            key_path: 配置键路径，支持嵌套键，如 'app.name'
            value: 配置值
            
        Returns:
            是否设置成功
        """
        keys = key_path.split('.')
        config = self.config_data
        
        try:
            # 导航到最后一个键的父级
            for key in keys[:-1]:
                if key not in config:
                    config[key] = {}
                config = config[key]
            
            # 设置值
            config[keys[-1]] = value
            self.logger.debug(f"设置配置: {key_path} = {value}")
            return True
        except Exception as e:
            self.logger.error(f"设置配置时出错: {str(e)}")
            return False
    
    def get_all(self):
        """获取所有配置
        
        Returns:
            配置字典
        """
        return self.config_data.copy()
    
    def set_all(self, config_data):
        """设置所有配置
        
        Args:
            config_data: 完整的配置字典
            
        Returns:
            是否设置成功
        """
        try:
            if isinstance(config_data, dict):
                self.config_data = config_data
                self.logger.info("设置所有配置成功")
                return True
            else:
                self.logger.error("配置数据必须是字典类型")
                return False
        except Exception as e:
            self.logger.error(f"设置所有配置时出错: {str(e)}")
            return False
    
    def remove(self, key_path):
        """删除配置项
        
        Args:
            key_path: 配置键路径
            
        Returns:
            是否删除成功
        """
        keys = key_path.split('.')
        config = self.config_data
        
        try:
            # 导航到最后一个键的父级
            for key in keys[:-1]:
                if key not in config:
                    return False
                config = config[key]
            
            # 删除键
            if keys[-1] in config:
                del config[keys[-1]]
                self.logger.debug(f"删除配置: {key_path}")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"删除配置时出错: {str(e)}")
            return False
