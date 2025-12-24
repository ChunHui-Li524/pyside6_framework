import os
import shutil
import json
import yaml
from datetime import datetime
from core.log_manager import LogManager
from utils.singleton import SingletonBase

class FileUtils(SingletonBase):
    """
    文件工具类，提供文件和目录操作的常用功能
    支持文件读写、目录操作、文件复制、移动、删除等功能
    """
    
    def __init__(self):
        """初始化文件工具类"""
        if hasattr(self, 'initialized'):
            return
            
        self.logger = LogManager()
        self.initialized = True
    
    def read_text_file(self, file_path, encoding='utf-8'):
        """读取文本文件
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
            
        Returns:
            文件内容字符串，失败返回None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                content = f.read()
            self.logger.debug(f"读取文件成功: {file_path}")
            return content
        except Exception as e:
            self.logger.error(f"读取文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    def write_text_file(self, file_path, content, encoding='utf-8', overwrite=True):
        """写入文本文件
        
        Args:
            file_path: 文件路径
            content: 文件内容
            encoding: 文件编码
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            是否写入成功
        """
        try:
            # 检查文件是否已存在
            if os.path.exists(file_path) and not overwrite:
                self.logger.warning(f"文件已存在且不允许覆盖: {file_path}")
                return False
            
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                self.logger.info(f"创建目录: {directory}")
            
            # 写入文件
            with open(file_path, 'w', encoding=encoding) as f:
                f.write(content)
            
            self.logger.debug(f"写入文件成功: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"写入文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    def read_json_file(self, file_path, encoding='utf-8'):
        """读取JSON文件
        
        Args:
            file_path: 文件路径
            encoding: 文件编码
            
        Returns:
            解析后的JSON对象，失败返回None
        """
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                data = json.load(f)
            self.logger.debug(f"读取JSON文件成功: {file_path}")
            return data
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON文件格式错误: {file_path}, 错误: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"读取JSON文件失败: {file_path}, 错误: {str(e)}")
            return None
    
    def write_json_file(self, file_path, data, encoding='utf-8', overwrite=True, indent=4):
        """写入JSON文件
        
        Args:
            file_path: 文件路径
            data: 要写入的数据
            encoding: 文件编码
            overwrite: 是否覆盖已存在的文件
            indent: 缩进空格数
            
        Returns:
            是否写入成功
        """
        try:
            # 检查文件是否已存在
            if os.path.exists(file_path) and not overwrite:
                self.logger.warning(f"文件已存在且不允许覆盖: {file_path}")
                return False
            
            # 确保目录存在
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
                self.logger.info(f"创建目录: {directory}")
            
            # 写入文件
            with open(file_path, 'w', encoding=encoding) as f:
                json.dump(data, f, ensure_ascii=False, indent=indent)
            
            self.logger.debug(f"写入JSON文件成功: {file_path}")
            return True
        except Exception as e:
            self.logger.error(f"写入JSON文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    def create_directory(self, directory_path):
        """创建目录
        
        Args:
            directory_path: 目录路径
            
        Returns:
            是否创建成功
        """
        try:
            if not os.path.exists(directory_path):
                os.makedirs(directory_path)
                self.logger.info(f"创建目录成功: {directory_path}")
                return True
            else:
                self.logger.warning(f"目录已存在: {directory_path}")
                return False
        except Exception as e:
            self.logger.error(f"创建目录失败: {directory_path}, 错误: {str(e)}")
            return False
    
    def list_files(self, directory_path, pattern='*', recursive=False):
        """列出目录中的文件
        
        Args:
            directory_path: 目录路径
            pattern: 文件匹配模式
            recursive: 是否递归列出
            
        Returns:
            文件路径列表
        """
        try:
            if not os.path.exists(directory_path):
                self.logger.warning(f"目录不存在: {directory_path}")
                return []
            
            import glob
            
            if recursive:
                search_path = os.path.join(directory_path, '**', pattern)
            else:
                search_path = os.path.join(directory_path, pattern)
            
            files = glob.glob(search_path, recursive=recursive)
            # 只返回文件，不包括目录
            files = [f for f in files if os.path.isfile(f)]
            
            self.logger.debug(f"列出目录文件: {directory_path}, 找到 {len(files)} 个文件")
            return files
        except Exception as e:
            self.logger.error(f"列出目录文件失败: {directory_path}, 错误: {str(e)}")
            return []
    
    def copy_file(self, source_path, destination_path, overwrite=True):
        """复制文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            是否复制成功
        """
        try:
            # 检查源文件是否存在
            if not os.path.exists(source_path):
                self.logger.error(f"源文件不存在: {source_path}")
                return False
            
            # 检查目标文件是否已存在
            if os.path.exists(destination_path) and not overwrite:
                self.logger.warning(f"目标文件已存在且不允许覆盖: {destination_path}")
                return False
            
            # 确保目标目录存在
            destination_dir = os.path.dirname(destination_path)
            if destination_dir and not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                self.logger.info(f"创建目录: {destination_dir}")
            
            # 复制文件
            shutil.copy2(source_path, destination_path)
            self.logger.debug(f"复制文件成功: {source_path} -> {destination_path}")
            return True
        except Exception as e:
            self.logger.error(f"复制文件失败: {source_path} -> {destination_path}, 错误: {str(e)}")
            return False
    
    def move_file(self, source_path, destination_path, overwrite=True):
        """移动文件
        
        Args:
            source_path: 源文件路径
            destination_path: 目标文件路径
            overwrite: 是否覆盖已存在的文件
            
        Returns:
            是否移动成功
        """
        try:
            # 检查源文件是否存在
            if not os.path.exists(source_path):
                self.logger.error(f"源文件不存在: {source_path}")
                return False
            
            # 检查目标文件是否已存在
            if os.path.exists(destination_path) and not overwrite:
                self.logger.warning(f"目标文件已存在且不允许覆盖: {destination_path}")
                return False
            
            # 确保目标目录存在
            destination_dir = os.path.dirname(destination_path)
            if destination_dir and not os.path.exists(destination_dir):
                os.makedirs(destination_dir)
                self.logger.info(f"创建目录: {destination_dir}")
            
            # 移动文件
            shutil.move(source_path, destination_path)
            self.logger.debug(f"移动文件成功: {source_path} -> {destination_path}")
            return True
        except Exception as e:
            self.logger.error(f"移动文件失败: {source_path} -> {destination_path}, 错误: {str(e)}")
            return False
    
    def delete_file(self, file_path):
        """删除文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否删除成功
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                self.logger.debug(f"删除文件成功: {file_path}")
                return True
            else:
                self.logger.warning(f"文件不存在: {file_path}")
                return False
        except Exception as e:
            self.logger.error(f"删除文件失败: {file_path}, 错误: {str(e)}")
            return False
    
    def get_file_info(self, file_path):
        """获取文件信息
        
        Args:
            file_path: 文件路径
            
        Returns:
            包含文件信息的字典
        """
        try:
            if not os.path.exists(file_path):
                self.logger.warning(f"文件不存在: {file_path}")
                return None
            
            stats = os.stat(file_path)
            return {
                'path': file_path,
                'name': os.path.basename(file_path),
                'size': stats.st_size,
                'created': datetime.fromtimestamp(stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                'modified': datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
                'accessed': datetime.fromtimestamp(stats.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
                'extension': os.path.splitext(file_path)[1].lower()
            }
        except Exception as e:
            self.logger.error(f"获取文件信息失败: {file_path}, 错误: {str(e)}")
            return None
