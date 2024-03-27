from PIL import Image
from ultralytics import YOLO
import os

os.chdir('C:\\projects\\Tagging-System')

# 사전 모델 불러오기 (상하의)
model = YOLO('models\\TOP&BOTTOM.pt')

# 폴더 생성
if not os.path.exists('new_label_data'):
    os.makedirs('new_label_data')

# 라벨 파일 폴더 생성
if not os.path.exists('new_label_data\\labels'):
    os.makedirs('new_label_data\\labels')

# 라벨 파일 폴더
labels_dir = 'new_label_data\\labels'

# 이미지 파일 폴더
images_dir = 'new_label_data\\images'
images_paths = [os.path.join(images_dir, img) for img in os.listdir(images_dir) if img.endswith(".png") or img.endswith("jpg")]

# 클래스 파일 생성
with open(f"{labels_dir}\\classes.txt", "w") as f:
    for name in model.names.values():
        f.write(f"{name}\n")

# 각 이미지 파일
for i in range(len(results)):

    # 탐지된 객체 값 구하기
    objects = results[i].boxes.xyxy

    # confidence, class_id 구하기
    confidence = results[i].boxes.conf
    class_id = results[i].boxes.cls