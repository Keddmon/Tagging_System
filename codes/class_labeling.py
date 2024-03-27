from PIL import Image
from ultralytics import YOLO
import os
import shutil # 이미지 복사



# 사전 모델 불러오기 (상하의)
model = YOLO('models\\TOP&BOTTOM.pt')

# 폴더 생성
if not os.path.exists('new_label_data'):
    os.makedirs('new_label_data')

# 라벨 파일 폴더 생성
if not os.path.exists('new_label_data\\labels'):
    os.makedirs('new_label_data\\labels')

# 이미지 파일 폴더 생성
if not os.path.exists('new_label_data\\images'):
    os.makedirs('new_label_data\\images')

# 라벨 파일 폴더
labels_dir = 'new_label_data\\labels'

# 이미지 파일 폴더
target_images_dir = 'new_label_data\\images' # 복사할 폴더
source_images_dir = 'test_images' # 원본 이미지 파일 폴더

for filename in os.listdir(source_images_dir):
    if filename.endswith('.png') or filename.endswith('jpg'):
        source_path = os.path.join(source_images_dir, filename)
        target_path = os.path.join(target_images_dir, filename)
        shutil.copyfile(source_path, target_path)

images_paths = [os.path.join(target_images_dir, img) for img in os.listdir(target_images_dir) if img.endswith(".png") or img.endswith("jpg")]

# 클래스 파일 생성
with open(f"{labels_dir}\\classes.txt", "w") as f:
    for name in model.names.values():
        f.write(f"{name}\n")

# 객체 탐지 결과
results = model(images_paths)

#################### 각 이미지에 대한 라벨 데이터 생성 및 정규화 ####################
# 각 이미지 파일
for i in range(len(results)):

    # 탐지된 객체 값 구하기
    objects = results[i].boxes.xyxy

    # confidence, class_id 구하기
    confidence = results[i].boxes.conf
    class_id = results[i].boxes.cls

    # 이미지 이름 구하기
    images_name = os.path.splitext(os.path.basename(images_paths[i]))[0]

    # 라벨 데이터 작성
    with open(f"{labels_dir}\\{images_name}.txt", "w") as f:
        for j in range(len(objects)):
            x1, y1, x2, y2 = objects[j]
            conf = confidence[j]
            cls_id = int(class_id[j])

            # 이미지 너비, 높이 구하기
            img = Image.open(images_paths[i])
            img_width, img_height = img.size

            # bounding box의 중심 좌표, 너비, 높이 계산
            x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
            y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
            width = round(((x2 - x1) / img_width).item(), 6)
            height = round(((y2 - y1) / img_height).item(), 6)

            f.write(f"{cls_id} {x_center} {y_center} {width} {height}\n")
#################################################################################

# 설정 파일 생성
if not os.path.exists('new_label_data\\dataset.yaml'):
    # dataset.yaml 파일 생성 코드
    f = open('new_label_data\\dataset.yaml', 'w')

with open("new_label_data\\dataset.yaml", "w") as f:
    f.write(f"train: images\n")  # 학습 이미지 경로
    f.write(f"val: images\n")  # 검증 이미지 경로
    f.write(f"nc: {len(model.names)}\n")  # 클래스 개수
    f.write(f"names: {list(model.names.values())}\n")  # 클래스 이름