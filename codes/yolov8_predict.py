from ultralytics import YOLO
import torch
import os

if __name__ == '__main__':

    # 이미지 폴더 위치
    # image_dir = 'codes/test_images/2022-11-0.jpg'
    image_dir = 'codes/test_images/2022-11-3.jpg'

    # 모델 불러오기
    model_path = os.path.join('models', 'TOP&BOTTOM(ver.3).pt')
    model = YOLO(model_path)

    # Predict
    results = model.predict(source = image_dir)

    for result in results:

        cls_list = result.boxes.cls.tolist()
        conf_list = result.boxes.conf.tolist()
        coords_list = result.boxes.xywhn

        unique_classes = [int(i) for i in torch.unique(result.boxes.cls).tolist()]
        highest_conf_boxes = []

        for cls in unique_classes:
            indices = [i for i, c in enumerate(cls_list) if c == cls]
        
            max_conf = 0
            max_conf_coords = None

            for i in indices:
                if conf_list[i] > max_conf:
                    max_conf = conf_list[i]
                    max_conf_coords = coords_list[i]

            highest_conf_boxes.append(cls)
            highest_conf_boxes.append(max_conf)
            highest_conf_boxes.append(max_conf_coords)

print(highest_conf_boxes)
