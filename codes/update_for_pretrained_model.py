from ultralytics import YOLO
from PIL import Image
import os
import shutil
import math

# 모델 불러오기
model_path = os.path.join('models', 'TOP&BOTTOM(ver.3).pt')
model = YOLO(model_path)

human_model_path = os.path.join('models', 'yolov8x.pt')
human_model = YOLO(human_model_path)

# 클래스 배열
class_mapping = []
for name in model.names.values():
    class_mapping.append(name)

# 폴더 생성
new_folder_index = 1
base_dir = f'new_label_data{new_folder_index}'
sub_dirs = ['train', 'val', 'test']
data_dirs = ['images', 'labels']
dir_paths = {}

while os.path.exists(base_dir):
    new_folder_index += 1
    base_dir = f'new_label_data{new_folder_index}'
    dir_paths['base_dir'] = base_dir

# 업로드 이미지 디렉토리
uploaded_images_dir = os.path.join('codes', 'test_images')

# 임시 테스트용
original_images_dir = os.path.join(base_dir, 'images')
os.makedirs(original_images_dir, exist_ok=True)
original_labels_dir = os.path.join(base_dir, 'labels')
os.makedirs(original_labels_dir, exist_ok=True)

# 서브 폴더 생성
for sub_dir in sub_dirs:
    dir_path = os.path.join(base_dir, sub_dir)
    dir_name = sub_dir
    os.makedirs(dir_path, exist_ok=True)

    dir_paths[dir_name] = os.path.abspath(dir_path)

    for data_dir in data_dirs:
        data_dir_path = os.path.join(dir_path, data_dir)
        data_dir_name = f'{sub_dir}_{data_dir}'
        os.makedirs(data_dir_path, exist_ok=True)

        dir_paths[data_dir_name] = os.path.abspath(data_dir_path)

# 객체 탐지 실패한 이미지 모아두기
failed_images_count = 0
failed_images_dir = os.path.join(base_dir, 'failed_images')
os.makedirs(failed_images_dir, exist_ok=True)

# 각 labels 폴더에 classes.txt 생성
classes_txts = [dir_paths['train_labels'], dir_paths['val_labels'], dir_paths['test_labels']]
for classes_txt in classes_txts:
    with open(os.path.join(classes_txt, 'classes.txt'), 'w') as f:
        for cls in class_mapping:
            f.write(f'{cls}\n')

image_files = sorted([filename for filename in os.listdir(uploaded_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
for filename in image_files:
    file_path = os.path.join(uploaded_images_dir, filename)
    # shutil.move(file_path, original_images_dir)
    # 임시 테스트용
    source_path = os.path.join(original_images_dir, filename)
    shutil.copyfile(file_path, source_path)
    
    # 임시 테스트용 (이미지 중 객체 탐지가 누락된 이미지 확인용)
    # file_results = model.predict(source=uploaded_images_dir, save=True)
    # for file_result in file_results:
    #     file_objects = file_result.boxes.xyxy
        # print(f'file_result: {file_objects}')

# 사전 모델 class의 index 추출
top_class_index = class_mapping.index('TOP')
bottom_class_index = class_mapping.index('BOTTOM')

batch_size = 50
num_batches = math.ceil(len(image_files) / batch_size)

for batch_i in range(num_batches):
    start_i = batch_i * batch_size
    end_i = min((batch_i + 1) * batch_size, len(image_files))
    batch_image_files = image_files[start_i:end_i]
    batch_image_paths = [os.path.join(original_images_dir, img) for img in batch_image_files]
    # batch_results = model.batch_image_paths

    # 테스트용
    batch_results = model.predict(source=batch_image_paths, conf=0.7, save=True)

    # 테스트용
    print('batch_results: ', len(batch_results))
    print('batch_image_paths: ', len(batch_image_paths))

    for image_path, result in zip(batch_image_paths, batch_results):
        images_name = os.path.splitext(os.path.basename(image_path))[0]
        objects = result.boxes.xyxy

        # 테스트용 (탐지된 이미지의 갯수)
        test_obj = []
        for obj in objects:
            test_obj += obj

        # 이미지 걸러내기
        cls_list = [int(x) for x in result.boxes.cls.tolist()]
        if len(objects) != 2:
            failed_images_count += 1
            shutil.move(image_path, failed_images_dir)
            continue
        elif 0 not in cls_list and 1 not in cls_list:
            failed_images_count += 1
            shutil.move(image_path, failed_images_dir)
            continue
      
        img = Image.open(image_path)
        img_width, img_height = img.size

        with open(f'{os.path.join(original_labels_dir, images_name)}.txt', 'w') as f:
            for i, object in enumerate(objects):
                box_class_item = int(result.boxes.cls[i].item())

                if box_class_item in [top_class_index, bottom_class_index]:
                    x1, y1, x2, y2 = object

                    x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
                    y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
                    width = round(((x2 - x1) / img_width).item(), 6)
                    height = round(((y2 - y1) / img_height).item(), 6)

                    if box_class_item == top_class_index:
                        class_index = class_mapping.index("TOP")
                    else:
                        class_index = class_mapping.index("BOTTOM")

                    f.write(f'{class_index} {x_center} {y_center} {width} {height}\n')

        img.close()

        # 이전 코드
        # with open(f'{os.path.join(original_labels_dir, images_name)}.txt', 'w') as f:
        #     for i, object in enumerate(objects):
        #         box_class_item = int(result.boxes.cls[i].item())

        #         img = Image.open(image_path)
        #         img_width, img_height = img.size

        #         if int(box_class_item) == top_class_index:
        #             x1, y1, x2, y2 = object

        #             x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
        #             y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
        #             width = round(((x2 - x1) / img_width).item(), 6)
        #             height = round(((y2 - y1) / img_height).item(), 6)

        #             f.write(f'{class_mapping.index("TOP")} {x_center} {y_center} {width} {height}\n')

        #         elif int(box_class_item) == bottom_class_index:
        #             x1, y1, x2, y2 = object

        #             x_center = round((((x1 + x2) / 2) / img_width).item(), 6)
        #             y_center = round((((y1 + y2) / 2) / img_height).item(), 6)
        #             width = round(((x2 - x1) / img_width).item(), 6)
        #             height = round(((y2 - y1) / img_height).item(), 6)

        #             f.write(f'{class_mapping.index("BOTTOM")} {x_center} {y_center} {width} {height}\n')

# dataset.yaml 생성
with open(os.path.join(base_dir, 'dataset.yaml'), 'w') as f:
    f.write(f'train: {dir_paths["train"]}\n')
    f.write(f'val: {dir_paths["val"]}\n')
    f.write(f'test: {dir_paths["test"]}\n')
    f.write(f'nc: {len(class_mapping)}\n')
    f.write(f'names: {class_mapping}\n')

# 테스트용
print('test_obj: ', len(test_obj))
print('failed_images_count: ', failed_images_count)