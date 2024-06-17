from ultralytics import YOLO
import os

if __name__ == '__main__':

    model_path = os.path.join('models', 'TOP&BOTTOM(ver.4).pt')

    data_path = os.path.join('API/new_label_data3', 'dataset.yaml')

    # 모델 불러오기
    model = YOLO(model_path)
    # model = YOLO('models\\yolov8n.pt')

    # 모델 학습
    train = model.train(data = data_path, epochs=1)