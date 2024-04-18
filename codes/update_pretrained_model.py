from PIL import Image
from ultralytics import YOLO
import os
import shutil

# 테스트
import string
import random



#################### 변수 선언 ####################



# 사전 모델 불러오기 (상하의)
model = YOLO('models//TOP&BOTTOM.pt')

# 테스트 (상하의 무작위 알파벳 지정)
alphabet = string.ascii_lowercase

# 클래스를 담을 배열
class_mapping = []

# 추가된 클래스를 담을 배열
additional_classes = []

# 실패한 이미지 갯수
failed_image_count = 0

# 폴더명
new_folder_name = 'new_label_data'
new_folder_index = 1

# TOP, BOTTOM 클래스 인덱스 변수 초기화
top_class_index = 0
bottom_class_index = 0



#################### 폴더 생성 및 주소 지정 ####################



# 데이터 폴더 생성
if os.path.exists(f'new_label_data{new_folder_index}'):
    new_folder_index += 1
os.makedirs(f'new_label_data{new_folder_index}')

# 라벨 데이터 폴더 생성
if not os.path.exists(f'new_label_data{new_folder_index}//labels'):
    os.makedirs(f'new_label_data{new_folder_index}//labels')
labels_dir = f'new_label_data{new_folder_index}//labels'

# 이미지 파일 폴더 생성
if not os.path.exists(f'new_label_data{new_folder_index}//images'):
    os.makedirs(f'new_label_data{new_folder_index}//images')
target_images_dir = f'new_label_data{new_folder_index}//images'  # 복사할 폴더
source_images_dir = 'test_images'  # 원본 이미지 파일 폴더

# 원본 이미지 파일 폴더의 이미지들을 복사할 폴더로 복사
image_files = sorted([filename for filename in os.listdir(source_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
for filename in image_files:
    source_path = os.path.join(source_images_dir, filename)
    target_path = os.path.join(target_images_dir, filename)
    shutil.copyfile(source_path, target_path)

# train, val, test 폴더 생성
# if not os.path.exists('new_label_data//images//train') and os.path.exists('new_label_data//images//val'):
#     os.makedirs('new_label_data//images//train')
#     os.makedirs('new_label_data//images//val')
# train_dir = 'new_label_data//images//train'
# val_dir = 'new_label_data//images//val'

# 실패한 이미지 폴더
if not os.path.exists(f'new_label_data{new_folder_index}//failed_images'):
    os.makedirs(f'new_label_data{new_folder_index}//failed_images')
failed_image_dir = f'new_label_data{new_folder_index}//failed_images'

# 클래스 파일 생성
with open(f"{labels_dir}//classes.txt", "w") as f:
    for name in model.names.values(): # 사전 모델의 클래스명을 불러옴
        f.write(f"{name}\n")
        class_mapping.append(name) # 불러온 클래스들을 배열에 담음

# print(f"top_class: {class_mapping.index('TOP')}")
# 사전 모델의 클래스 인덱스 번호
top_class_index = class_mapping.index('TOP')
bottom_class_index = class_mapping.index('BOTTOM')



#################### 객체 탐지 결과 ####################



# 각 이미지를 사전 모델을 통해 객체 탐지
results = model([os.path.join(target_images_dir, img) for img in image_files])



#################### 각 이미지에 대한 라벨 데이터 생성 ####################



for image_path, result in zip([os.path.join(target_images_dir, img) for img in image_files], results):


    # 이미지 이름 뽑아오기
    images_name = os.path.splitext(os.path.basename(image_path))[0]
    print(f"Image: {images_name}")

    # 이미지당 탐지된 바운딩박스의 x, y 좌표
    objects = result.boxes.xyxy
    print(f"obejcts:{objects}")

    # 객체 탐지 오류 이미지 걸러내기
    if len(objects) != 2:
        print("실패, 객체가 1개 또는 3개 이상 탐지됨.")
        failed_image_count += 1
        shutil.move(image_path, failed_image_dir)
        continue

    # 이미지당 객체에 대한 라벨 데이터 작성
    with open(f"{labels_dir}//{images_name}.txt", "w") as f:
        # for obj in objects:
        #     print(obj)
        #     if top_class:
        
        for i, obj in enumerate(objects):
            print(f'class_name: {result.names[0], result.names[1]}')
            print(f'obj: {obj}')
            print(f'box_class: {result.boxes.cls[0].item(), result.boxes.cls[1].item()}')

            # 탐지된 객체의 클래스 인덱스 번호
            # first_box_class = int(result.boxes.cls[0].item())
            # second_box_clss = int(result.boxes.cls[1].item())
            box_class_item = int(result.boxes.cls[i].item())

            # 이미지 너비, 높이 구하기
            img = Image.open(image_path)
            img_width, img_height = img.size

            if int(box_class_item) == top_class_index:
                x1, y1, x2, y2 = obj
                # print(f"objects:{obj}")
                # x1, y1, x2, y2 = obj # x1, y1 = 왼쪽 위 모서리, x2, y2 = 오른쪽 아래 모서리
     
                # bounding box의 중심 좌표, 너비, 높이 계산
                x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                width = round(((x2 - x1) / img_width).item(), 6)
                height = round(((y2 - y1) / img_height).item(), 6)

                # 라벨 데이터 작성
                # images_name = os.path.splitext(os.path.basename(image_path))[0]
                # with open(f"{labels_dir}//{images_name}.txt", "w") as f:
                f.write(f"{top_class_index} {x_center} {y_center} {width} {height}\n")

            elif int(box_class_item) == bottom_class_index: 
                x1, y1, x2, y2 = obj
                # print(f"objects:{obj}")
                # x1, y1, x2, y2 = obj # x1, y1 = 왼쪽 위 모서리, x2, y2 = 오른쪽 아래 모서리
    
                # bounding box의 중심 좌표, 너비, 높이 계산
                x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                width = round(((x2 - x1) / img_width).item(), 6)
                height = round(((y2 - y1) / img_height).item(), 6)

                # 라벨 데이터 작성
                # images_name = os.path.splitext(os.path.basename(image_path))[0]
                # with open(f"{labels_dir}//{images_name}.txt", "w") as f:
                f.write(f"{bottom_class_index} {x_center} {y_center} {width} {height}\n")

# dataset.yaml 파일 생성
if not os.path.exists(f'new_label_data{new_folder_index}//dataset.yaml'):
    with open(f"new_label_data{new_folder_index}//dataset.yaml", "w") as f:
        f.write(f"train: images\n")  # 학습 이미지 경로
        f.write(f"val: images\n")  # 검증 이미지 경로
        f.write(f"nc: {len(model.names)}\n")  # 클래스 개수
        f.write(f"names: {list(model.names.values())}\n")  # 클래스 이름