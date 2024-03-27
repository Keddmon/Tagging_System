from ultralytics import YOLO

# 이미지 폴더 위치
source = 'test_images'

# 모델 학습
train = model.train('dataset.yaml', ephochs=10, device=0)

# 모델 불러오기
model = YOLO('TOP&BOTTOM.pt')

# Predict
results = model.predict(source, save=True)