from PIL import Image
from ultralytics import YOLO
import os
import shutil
import math
import string
import random

model = YOLO('models//TOP&BOTTOM(ver.4).pt')

alphabet = string.ascii_lowercase

class_mapping = []

additional_classes = []

failed_image_count = 0

new_folder_name = 'new_label_data'
new_folder_index = 1

top_class_index = 0
bottom_class_index = 0

batch_size = 100

if os.path.exists(f'new_label_data{new_folder_index}'):
    new_folder_index += 1
os.makedirs(f'new_label_data{new_folder_index}')

if not os.path.exists(f'new_label_data{new_folder_index}//labels'):
    os.makedirs(f'new_label_data{new_folder_index}//labels')
labels_dir = f'new_label_data{new_folder_index}//labels'

if not os.path.exists(f'new_label_data{new_folder_index}//images'):
    os.makedirs(f'new_label_data{new_folder_index}//images')
target_images_dir = f'new_label_data{new_folder_index}//images'
source_images_dir = 'test_images'

image_files = sorted([filename for filename in os.listdir(source_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
for filename in image_files:
    source_path = os.path.join(source_images_dir, filename)
    target_path = os.path.join(target_images_dir, filename)
    shutil.copyfile(source_path, target_path)

if not os.path.exists(f'new_label_data{new_folder_index}//failed_images'):
    os.makedirs(f'new_label_data{new_folder_index}//failed_images')
failed_image_dir = f'new_label_data{new_folder_index}//failed_images'

with open(f"{labels_dir}//classes.txt", "w") as f:
    for name in model.names.values():
        f.write(f"{name}\n")
        class_mapping.append(name)
top_class_index = class_mapping.index('TOP')
bottom_class_index = class_mapping.index('BOTTOM')

num_batches = math.ceil(len(image_files) / batch_size)

for batch_idx in range(num_batches):
    start_idx = batch_idx * batch_size
    end_idx = min((batch_idx + 1) * batch_size, len(image_files))
    batch_image_files = image_files[start_idx:end_idx]
    batch_results = model([os.path.join(target_images_dir, img) for img in batch_image_files])

    for image_path, result in zip([os.path.join(target_images_dir, img) for img in batch_image_files], batch_results):
        
        images_name = os.path.splitext(os.path.basename(image_path))[0]
              
        # 탐지된 객체의 Bounding box 좌표
        objects = result.boxes.xyxy
        
        # 탐지된 객체의 Bounding box 중 각 클래스별로 가장 높은 신뢰도를 선택
        best_conf = {}
        best_boxes = {}

        conf_list = result.boxes.conf.tolist()
        cls_list = result.boxes.cls.tolist()
        coords_list = result.boxes.xyxy.tolist()

        for i, (confidence, cls, box) in enumerate(zip(conf_list, cls_list, coords_list)):
            if cls not in best_conf or confidence > best_conf[cls]:
                best_conf[cls] = confidence
                best_boxes[cls] = box
        # if len(objects) != 2:
            
        #     failed_image_count += 1
        #     shutil.move(image_path, failed_image_dir)
        #     continue

        # 임시 테스트용
        top_category = random.choice(alphabet[:13])
        bottom_category = random.choice(alphabet[13:])
        
        if top_category not in class_mapping:
            class_mapping.append(top_category)
            additional_classes.append(top_category)
        if bottom_category not in class_mapping:
            class_mapping.append(bottom_category)
            additional_classes.append(bottom_category)
       
        with open(f"{labels_dir}//{images_name}.txt", "w") as f:
                        
            for i, obj in enumerate(objects):
            
                box_class_item = int(result.boxes.cls[i].item())

                img = Image.open(image_path)
                img_width, img_height = img.size
                

                if int(box_class_item) == top_class_index:
                    x1, y1, x2, y2 = obj

                    x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                    y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                    width = round(((x2 - x1) / img_width).item(), 6)
                    height = round(((y2 - y1) / img_height).item(), 6)

                    f.write(f"{class_mapping.index(top_category)} {x_center} {y_center} {width} {height}\n")

                elif int(box_class_item) == bottom_class_index: 
                    x1, y1, x2, y2 = obj

                    x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                    y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                    width = round(((x2 - x1) / img_width).item(), 6)
                    height = round(((y2 - y1) / img_height).item(), 6)

                    f.write(f"{class_mapping.index(bottom_category)} {x_center} {y_center} {width} {height}\n")

with open(f"{labels_dir}//classes.txt", "a") as f:
    for cls in additional_classes:
        f.write(f"{cls}\n")

if not os.path.exists(f'new_label_data{new_folder_index}//dataset.yaml'):
    with open(f"new_label_data{new_folder_index}//dataset.yaml", "w") as f:
        f.write(f"train: images\n")
        f.write(f"val: images\n")
        f.write(f"nc: {len(model.names) + len(additional_classes)}\n")
        f.write(f"names: {list(model.names.values()) + additional_classes}\n")