from ultralytics import YOLO
import os
import torch

model_path = os.path.join('models', 'TOP&BOTTOM(ver.4).pt')
model = YOLO(model_path)

images_path = 'test_images'

images_list = os.listdir(images_path)

results = model.predict(source=images_path)

print(results[0])

for result in results:
    objects = result.boxes.xyxy

    for i, object in enumerate(objects):
        box_class_item = int(result.boxes.cls[i].item())
        x1, y1, x2, y2 = object

        # print(x1, y1, x2, y2)

for result in results:
    # print(r.boxes.conf)
    # print(r.boxes.xyxy)
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

    # for cls, (conf, coords) in highest_conf_boxes.items():
    #     class_name = 'TOP' if cls == 0 else 'BOTTOM'
    # print(len(highest_conf_boxes))
    # print(len(highest_conf_cls))
    for i in range(len(highest_conf_boxes)):
        x1, y1, x2, y2 = highest_conf_boxes[i]
        # print(x1, y1 ,x2, y2)
        # print(highest_conf_cls[i])
        # print(f'{class_name}: 신뢰도={conf}, 좌표={coords}')
    # for cls, conf in enumerate(r.boxes.cls.tolist(), r.boxes.conf.tolist())
    