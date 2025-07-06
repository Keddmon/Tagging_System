from ultralytics import YOLO
import os
import cv2
import numpy as np
from tqdm import tqdm
import pandas as pd

# 경로 설정
BASE_DIR = 'API'
IMAGE_DIR = os.path.join(BASE_DIR, 'images')
OUTPUT_LABEL_DIR = os.path.join(BASE_DIR, 'labels')
OUTPUT_VIS_DIR = os.path.join(BASE_DIR, 'visualized')
FAILED_LIST_PATH = os.path.join(BASE_DIR, 'failed_images.txt')
FAILED_LOG_CSV = os.path.join(BASE_DIR, 'failed_log.csv')

MODEL_PATH = os.path.join(BASE_DIR, 'TOP&BOTTOM(ver.4).pt')

# 실패 유형별 폴더 설정
FAILED_DIR = os.path.join(BASE_DIR, 'failed')
FAILED_DIRS = {
    'none_detected': os.path.join(FAILED_DIR, 'none_detected'),
    'missing_class': os.path.join(FAILED_DIR, 'missing_class'),
    'low_confidence': os.path.join(FAILED_DIR, 'low_confidence'),
    'wrong_position': os.path.join(FAILED_DIR, 'wrong_position'),
}

# 디렉토리 생성
os.makedirs(OUTPUT_LABEL_DIR, exist_ok=True)
os.makedirs(OUTPUT_VIS_DIR, exist_ok=True)
for path in FAILED_DIRS.values():
    os.makedirs(path, exist_ok=True)

# 모델 로드
model = YOLO(MODEL_PATH)

# 실패 저장용
failed_images = []
failed_logs = []

# 이미지 리스트
image_files = [f for f in os.listdir(IMAGE_DIR) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]

# 처리 루프
for img_file in tqdm(image_files, desc="Processing"):
    img_path = os.path.join(IMAGE_DIR, img_file)
    img = cv2.imread(img_path)
    h, w = img.shape[:2]

    result = model(img_path, verbose=False)[0]
    boxes = result.boxes

    # 감지 결과 없음
    if boxes is None or boxes.data.shape[0] == 0:
        failed_images.append(f"{img_file} - No detections")
        fail_path = os.path.join(FAILED_DIRS['none_detected'], img_file)
        cv2.imwrite(fail_path, img)
        failed_logs.append({
            'filename': img_file,
            'reason': 'No detections',
            'top_conf': None,
            'bottom_conf': None,
            'top_cy': None,
            'bottom_cy': None
        })
        continue

    # 클래스별 박스 필터링
    top_boxes = [b for b in boxes.data if int(b[5]) == 0]
    bottom_boxes = [b for b in boxes.data if int(b[5]) == 1]

    # 둘 중 하나라도 감지되지 않음
    if len(top_boxes) == 0 or len(bottom_boxes) == 0:
        failed_images.append(f"{img_file} - Missing TOP or BOTTOM")
        fail_path = os.path.join(FAILED_DIRS['missing_class'], img_file)
        for b in boxes.data:
            x1, y1, x2, y2 = map(int, b[0:4])
            conf = float(b[4])
            cls = int(b[5])
            label = f"{'TOP' if cls == 0 else 'BOTTOM'} {conf:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imwrite(fail_path, img)

        failed_logs.append({
            'filename': img_file,
            'reason': 'Missing TOP or BOTTOM',
            'top_conf': float(top_boxes[0][4]) if top_boxes else None,
            'bottom_conf': float(bottom_boxes[0][4]) if bottom_boxes else None,
            'top_cy': float((top_boxes[0][1] + top_boxes[0][3]) / 2) if top_boxes else None,
            'bottom_cy': float((bottom_boxes[0][1] + bottom_boxes[0][3]) / 2) if bottom_boxes else None
        })
        continue

    # 가장 높은 confidence 박스만 사용
    top = max(top_boxes, key=lambda x: x[4])
    bottom = max(bottom_boxes, key=lambda x: x[4])

    # 추가 조건: 위치 및 신뢰도 기준
    top_conf = float(top[4])
    bottom_conf = float(bottom[4])
    top_cy = float((top[1] + top[3]) / 2)
    bottom_cy = float((bottom[1] + bottom[3]) / 2)

    if top_cy >= bottom_cy:
        failed_images.append(f"{img_file} - TOP not above BOTTOM")
        fail_path = os.path.join(FAILED_DIRS['wrong_position'], img_file)
        for b in boxes.data:
            x1, y1, x2, y2 = map(int, b[0:4])
            conf = float(b[4])
            cls = int(b[5])
            label = f"{'TOP' if cls == 0 else 'BOTTOM'} {conf:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imwrite(fail_path, img)

        failed_logs.append({
            'filename': img_file,
            'reason': 'TOP not above BOTTOM',
            'top_conf': top_conf,
            'bottom_conf': bottom_conf,
            'top_cy': top_cy,
            'bottom_cy': bottom_cy
        })
        continue

    if top_conf < 0.5 or bottom_conf < 0.5:
        failed_images.append(f"{img_file} - Low confidence (TOP: {top_conf:.2f}, BOTTOM: {bottom_conf:.2f})")
        fail_path = os.path.join(FAILED_DIRS['low_confidence'], img_file)
        for b in boxes.data:
            x1, y1, x2, y2 = map(int, b[0:4])
            conf = float(b[4])
            cls = int(b[5])
            label = f"{'TOP' if cls == 0 else 'BOTTOM'} {conf:.2f}"
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        cv2.imwrite(fail_path, img)

        failed_logs.append({
            'filename': img_file,
            'reason': 'Low confidence',
            'top_conf': top_conf,
            'bottom_conf': bottom_conf,
            'top_cy': top_cy,
            'bottom_cy': bottom_cy
        })
        continue

    # 라벨 저장 함수
    def convert_to_yolo(box, class_id):
        x1, y1, x2, y2 = box[0:4]
        cx = ((x1 + x2) / 2) / w
        cy = ((y1 + y2) / 2) / h
        bw = (x2 - x1) / w
        bh = (y2 - y1) / h
        return f"{class_id} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}"

    # 라벨 저장
    label_path = os.path.join(OUTPUT_LABEL_DIR, os.path.splitext(img_file)[0] + ".txt")
    with open(label_path, 'w') as f:
        f.write(convert_to_yolo(top, 0) + "\n")
        f.write(convert_to_yolo(bottom, 1) + "\n")

    # 시각화
    for box, class_id in zip([top, bottom], [0, 1]):
        x1, y1, x2, y2 = map(int, box[0:4])
        conf = float(box[4])
        label = f"{'TOP' if class_id == 0 else 'BOTTOM'} {conf:.2f}"
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(img, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    vis_path = os.path.join(OUTPUT_VIS_DIR, img_file)
    cv2.imwrite(vis_path, img)

# 실패 이미지 목록 저장
with open(FAILED_LIST_PATH, 'w') as f:
    for entry in failed_images:
        f.write(entry + '\n')

# 실패 상세 로그 CSV 저장
if failed_logs:
    df = pd.DataFrame(failed_logs)
    df.to_csv(FAILED_LOG_CSV, index=False)
    print(f"\n📄 실패 로그 저장 완료: {FAILED_LOG_CSV}")

print(f"\n✅ 전처리 완료: {len(image_files) - len(failed_images)} 성공 / {len(failed_images)} 실패")