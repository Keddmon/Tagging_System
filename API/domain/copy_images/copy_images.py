from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import shutil
import os

#BaseModel
class TargetDir(BaseModel):
    dir: str

router = APIRouter(
    prefix="/api/copyimages",
    tags={"copy images source to target"}
)

@router.post("/copy-images")
async def copy_images(directory: TargetDir):
    target_dir = directory.dir

    source_images_dir = "uploaded_files"

    if not os.path.exists(source_images_dir):
        raise HTTPException(status_code=404, detail=f"Source Directory '{source_images_dir}' not found.")

    target_images_dir = os.path.join(target_dir, "images")

    image_files = sorted([filename for filename in os.listdir(source_images_dir) if filename.endswith('.png') or filename.endswith('.jpg')])
    for filename in image_files:
        source_path = os.path.join(source_images_dir, filename)
        target_path = os.path.join(target_images_dir, filename)
        shutil.copyfile(source_path, target_path)

    return {'image_files': image_files}