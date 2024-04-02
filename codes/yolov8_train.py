from ultralytics import YOLO

if __name__ == '__main__':

    # 모델 불러오기
    # model = YOLO('models\\TOP&BOTTOM.pt')
    model = YOLO('models\\TOP&BOTTOM.pt')

    # 모델 학습
    train = model.train(data = 'new_label_data\\dataset.yaml', epochs=50)