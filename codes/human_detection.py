from ultralytics import YOLO
import os
from PIL import Image

model_path = os.path.join('models', 'TOP&BOTTOM(ver.3).pt')
model = YOLO(model_path)
crop_images_dir = "runs/detect/predict/crops/person"
model.predict(source=crop_images_dir, save=True)

human_model_path = os.path.join('models', 'yolov8x.pt')
human_model = YOLO(human_model_path)
human_index = 0
test_images_dir = os.path.join('codes', 'test_images')


# results = human_model.predict(
#     source=test_images_dir,
#     classes=[human_index],
#     conf=0.9,
#     save_txt=True,
# )
results = human_model.predict(
    source = test_images_dir,
    classes = [human_index],
    conf = 0.9,
    # save_txt = True,
    # save_crop = True
)

image_files = sorted([filename for filename in os.listdir(test_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
for filename in image_files:
    file_path = os.path.join(test_images_dir, filename)
    img = Image.open(file_path)
    img_width, img_height = img.size

    objects = human_model.predict(source=file_path, classes=[human_index], conf=0.9)

    for obj in objects:
        obj = obj.boxes.xyxy
        
        for coordinate in obj:
            x1, y1, x2, y2 = coordinate
        print(coordinate)
        img = Image.open(file_path)
        img_width, img_height = img.size

        x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
        y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
        width = round(((x2 - x1) / img_width).item(), 6)
        height = round(((y2 - y1) / img_height).item(), 6)

        print(x_center, y_center, width, height)