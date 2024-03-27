from ultralytics import YOLO

if __name__ == '__main__':

    # 이미지 폴더 위치
    source = 'test_images'

    # 모델 불러오기
    model = YOLO('runs\\detect\\train\\weights\\best.pt')

    # Predict
    results = model.predict(source, save=True)