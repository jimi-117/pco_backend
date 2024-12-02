# tests/fixtures/setup_model.py
from ultralytics import YOLO
import yaml
import shutil
import os

def setup_test_model():
    # 
    model = YOLO('yolo11l.pt')
    
    # モデルをテストディレクトリにコピー
    os.makedirs('tests/fixtures/models', exist_ok=True)
    shutil.copy('yolov8n.pt', 'tests/fixtures/models/yolov8n.pt')
    
    # モデル設定を保存
    model_config = {
        "model_type": "yolov8n",
        "classes": model.names,
        "version": "8.0.0",
        "input_size": 640
    }
    
    with open('tests/fixtures/models/model_config.yaml', 'w') as f:
        yaml.dump(model_config, f)

if __name__ == "__main__":
    setup_test_model()
