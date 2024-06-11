from fastapi import APIRouter, UploadFile, File
import os
from typing import List
import shutil

router = APIRouter(
    prefix="/api/uploadfiles",
    tags=["uploadfiles"],
)

@router.post("/upload-files")
async def upload_images(images: List[UploadFile] = File(...), jsons: List[UploadFile] = File(...)):
    if not os.path.exists("uploaded_files"):
        os.makedirs("uploaded_files")

    if len(images) != len(jsons):
        return {"error": "이미지 파일과 JSON 파일의 개수가 동일하지 않습니다."}
    
    image_locations = []
    json_locations = []

    for image, json in zip(images, jsons):
        # 이미지 업로드
        image_location = os.path.join("uploaded_files", image.filename)
        with open(image_location, "wb") as image_object:
            shutil.copyfileobj(image.file, image_object)
        image_locations.append(image_location)

        # JSON 업로드
        json_location = os.path.join("uploaded_files", json.filename)
        with open(json_location, "wb") as json_object:
            shutil.copyfileobj(json.file, json_object)
        json_locations.append(json_location)
    
    return {"image_locations": image_locations, "json_locations": json_locations}