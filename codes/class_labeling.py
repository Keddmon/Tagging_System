from PIL import Image
from ultralytics import YOLO
import os
import shutil

# 테스트
import string
import random

#################### 변수 선언 ####################

# 클래스를 담을 배열
class_mapping = []

# 추가된 클래슬르 담을 배열
additional_classes = []

# 실패한 이미지 갯수
failed_image_count = 0

# 사전 모델 불러오기 (상하의)
model = YOLO('models//TOP&BOTTOM.pt')

# 테스트
alphabet = string.ascii_lowercase

#################### 폴더 생성 및 주소 지정 ####################

# 라벨 데이터 폴더 생성
if not os.path.exists('new_label_data'):
    os.makedirs('new_label_data')

# 라벨 데이터 폴더 생성
if not os.path.exists('new_label_data//labels'):
    os.makedirs('new_label_data//labels')
labels_dir = 'new_label_data//labels'

# 이미지 파일 폴더 생성
if not os.path.exists('new_label_data//images'):
    os.makedirs('new_label_data//images')
target_images_dir = 'new_label_data//images'  # 복사할 폴더
source_images_dir = 'test_images'  # 원본 이미지 파일 폴더

# 실패한 이미지 폴더
if not os.path.exists('new_label_data//failed_images'):
    os.makedirs('new_label_data//failed_images')
failed_image_dir = 'new_label_data//failed_images'

# 클래스 파일 생성
with open(f"{labels_dir}//classes.txt", "w") as f:
    for name in model.names.values():
        f.write(f"{name}\n")
        class_mapping.append(name)

# 원본 이미지 파일 폴더의 이미지들을 복사할 폴더로 복사
image_files = sorted([filename for filename in os.listdir(source_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
for filename in os.listdir(source_images_dir):
    source_path = os.path.join(source_images_dir, filename)
    target_path = os.path.join(target_images_dir, filename)
    shutil.copyfile(source_path, target_path)

#################### 객체 탐지 결과 ####################
    
results = model([os.path.join(target_images_dir, img) for img in image_files])
model.predict(source='new_label_data//images', save=True)

#################### 각 이미지에 대한 라벨 데이터 생성 ####################

for image_path, result in zip([os.path.join(target_images_dir, img) for img in image_files], results):

    images_name = os.path.splitext(os.path.basename(image_path))[0]

    print(f"Image: {images_name}")

    # 이미지당 탐지된 객체의 개수 확인
    objects = result.boxes.xyxy
    if len(objects) != 2:
        print("실패, 객체가 3개 이상 탐지됨.")
        failed_image_count += 1
        shutil.move(image_path, failed_image_dir)
        continue

    # 이미지와 함께 각각의 이미지 내에 존재하는 패션 아이템의 상의와 하의 종류 입력 받기 (테스트)
    # top_category = input("Enter the TOP category: ")
    # bottom_category = input("Enter the bottom category: ")

    top_category = random.choice(alphabet[:13])
    bottom_category = random.choice(alphabet[13:])

    # 새로운 클래스 추가
    if top_category not in class_mapping:
        class_mapping.append(top_category)
        additional_classes.append(top_category)
    if bottom_category not in class_mapping:
        class_mapping.append(bottom_category)
        additional_classes.append(bottom_category)

    # 이미지당 객체에 대한 라벨 데이터 작성
    with open(f"{labels_dir}//{images_name}.txt", "w") as f:
        for obj in objects: 
            x1, y1, x2, y2 = obj

            # 이미지 너비, 높이 구하기
            img = Image.open(image_path)
            img_width, img_height = img.size

            # bounding box의 중심 좌표, 너비, 높이 계산
            x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
            y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
            width = round(((x2 - x1) / img_width).item(), 6)
            height = round(((y2 - y1) / img_height).item(), 6)

            # 라벨 데이터 작성
            images_name = os.path.splitext(os.path.basename(image_path))[0]
            with open(f"{labels_dir}//{images_name}.txt", "w") as f:
                f.write(f"{class_mapping.index(top_category)} {x_center} {y_center} {width} {height}\n")
                f.write(f"{class_mapping.index(bottom_category)} {x_center} {y_center} {width} {height}\n")

# 클래스 파일 업데이트
with open(f"{labels_dir}//classes.txt", "a") as f:
    for cls in additional_classes:
        f.write(f"{cls}\n")

# dataset.yaml 파일 생성
if not os.path.exists('new_label_data//dataset.yaml'):
    with open("new_label_data//dataset.yaml", "w") as f:
        f.write(f"train: images\n")  # 학습 이미지 경로
        f.write(f"val: images\n")  # 검증 이미지 경로
        f.write(f"nc: {len(model.names) + len(additional_classes)}\n")  # 클래스 개수
        f.write(f"names: {list(model.names.values()) + additional_classes}\n")  # 클래스 이름
