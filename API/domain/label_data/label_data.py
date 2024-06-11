from fastapi import APIRouter
from pydantic import BaseModel
import os

# BaseModel
class LabelDataDir(BaseModel):
    target_dir: str
    labels_dir: str
    images_dir: str
    class_mapping: list

router = APIRouter(
    prefix="/api/labeldata",
    tags={"generate classes.txt and dataset.yaml"}
)

@router.post("/label-data")
async def label_data(request: LabelDataDir):

    target_dir = request.target_dir
    images_dir = request.images_dir
    labels_dir = request.labels_dir
    class_mapping = request.class_mapping

    with open(os.path.join(labels_dir, 'classes.txt'), 'w') as f:
        for cls in class_mapping:
            f.write(f'{cls}\n')

    with open(os.path.join(target_dir, 'dataset.yaml'), 'w') as f:
        f.write(f'train: {images_dir}\n')
        f.write(f'val: images\n')
        f.write(f'nc: {len(class_mapping)}\n')
        f.write(f'names: {class_mapping}\n')