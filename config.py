# config.py
from dotenv import load_dotenv
import os

# 加载.env文件中的环境变量（默认读取当前目录的.env）
load_dotenv()

# 读取敏感配置（key不存在时返回None，可加默认值）
API_KEY = os.getenv("Qwen_API_KEY")

# 可选：验证必要配置是否存在，避免运行时出错
def validate_config():
    required_keys = ["Qwen_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    if missing_keys:
        raise ValueError(f"缺少必要配置项：{', '.join(missing_keys)}")

# 初始化时验证配置
validate_config()