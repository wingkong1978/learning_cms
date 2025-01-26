import os
import sys

# 将项目根目录添加到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app import db, app  # 从 app.py 中导入 db 和 app
from backend.config import Config  # 确保导入 Config

# 确保 app 使用正确的配置
app.config.from_object(Config)

with app.app_context():
    db.create_all()
    print("Database initialized successfully!") 