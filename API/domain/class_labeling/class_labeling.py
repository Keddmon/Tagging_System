from fastapi import APIRouter
from pydantic import BaseModel
from ultralytics import YOLO
from PIL import Image
import os
import shutil
import math
import torch
import json

# BaseModel
class ClassLabelingDir(BaseModel):
    images_dir: str
    labels_dir: str
    failed_images_dir: str
    image_files: list
    json_files: list

router = APIRouter(
    prefix="/api/classlabeling",
    tags={"predict images and labeling"}
)

@router.post("/class-labeling")
async def class_labeling(request: ClassLabelingDir):

    images_dir = request.images_dir
    labels_dir = request.labels_dir
    failed_images_dir = request.failed_images_dir
    image_files = request.image_files
    json_files = request.json_files

    model = YOLO(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'TOP&BOTTOM(ver.4).pt'))

    class_mapping = []
    failed_images_count = 0
    
    # 임시 테스트용: JSON 파일 정렬
    json_files.sort()

    # 전체 이미지 수를 배치 크기만큼 나눠서 진행
    batch_size = 100
    num_batches = math.ceil(len(image_files) / batch_size)

    # 사전 모델에서 정의된 클래스들을 리스트에 추가
    for name in model.names.values():
        class_mapping.append(name)

    # 사전 모델의 TOP 및 BOTTOM 클래스 인덱스 번호 가져오기
    top_class_index = class_mapping.index('TOP')
    bottom_class_index = class_mapping.index('BOTTOM')

    for batch_i in range(num_batches):
        start_i = batch_i * batch_size
        end_i = min((batch_i + 1) * batch_size, len(image_files))
        batch_image_files = image_files[start_i:end_i]
        batch_json_files = json_files[start_i:end_i]

        batch_results = model.predict(source=[os.path.join(images_dir, img) for img in batch_image_files], save=True)

        for image_path, json_file in zip([os.path.join(images_dir, img) for img in batch_image_files], batch_json_files):

        # for image_path, result in zip([os.path.join(images_dir, img) for img in batch_image_files], batch_results):

            images_name = os.path.splitext(os.path.basename(image_path))[0]

            with open(json_file, 'r') as json_file:
                json_data = json.load(json_file)

            # 클래스별 가장 높은 신뢰도를 가진 Bounding box 찾기
            result = batch_results[image_files.index(os.path.basename(image_path))]
            cls_list = result.boxes.cls.tolist()
            conf_list = result.boxes.conf.tolist()
            coords_list = result.boxes.xyxy

            unique_classes = [int(i) for i in torch.unique(result.boxes.cls).tolist()]
            highest_conf_boxes = []
            highest_conf_cls = []

            for cls in unique_classes:
                indices = [i for i, c in enumerate(cls_list) if c == cls]
            
                max_conf = 0
                max_conf_coords = None

                for i in indices:
                    if conf_list[i] > max_conf:
                        max_conf = conf_list[i]
                        max_conf_coords = coords_list[i]

                highest_conf_boxes.append(max_conf_coords)
                highest_conf_cls.append(cls)

            top_category = json_data['categories'][0]['category']
            bottom_category = json_data['categories'][1]['category']

            # 패션 아이템 카테고리를 클래스에 추가, 중복 시 추가X
            if top_category not in class_mapping:
                class_mapping.append(top_category)
            if bottom_category not in class_mapping:
                class_mapping.append(bottom_category)

            # txt 어노테이션 데이터 생성
            with open(f'{os.path.join(labels_dir, images_name)}.txt', 'w') as f:
                img = Image.open(image_path)
                img_width, img_height = img.size

                for i in range(len(highest_conf_boxes)):
                    x1, y1, x2, y2 = highest_conf_boxes[i]

                    x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                    y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                    width = round(((x2 - x1) / img_width).item(), 6)
                    height = round(((y2 - y1) / img_height).item(), 6)

                    if highest_conf_cls[i] == top_class_index:
                        class_index = class_mapping.index(top_category)
                    elif highest_conf_cls[i] == bottom_class_index:
                        class_index = class_mapping.index(bottom_category)

                    f.write(f"{class_index} {x_center} {y_center} {width} {height}\n")
                    # x1 + x2 = 2 * x_center * img_width
  
    return {'class_mapping': class_mapping}