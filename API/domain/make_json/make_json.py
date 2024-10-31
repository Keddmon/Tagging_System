from fastapi import APIRouter
from pydantic import BaseModel
import os
import json

# BaseModel
class Categories(BaseModel):
    image_name: str
    top_category: str
    bottom_category: str

router = APIRouter(
    prefix="/api/makejson",
    tags={"generate JSON of Top and Bottom categories"}
)

@router.post("/make-json")
async def make_json(request: Categories):

    image_name = request.image_name
    top_category = request.top_category
    bottom_category = request.bottom_category

    data = {
        "image": image_name,
        "categories": [
            {
                "item": "top",
                "category": top_category
            },
            {
                "item": "bottom",
                "category": bottom_category
            }
        ]
    }

    file_path = os.path.join('createdJson', f'{image_name}.json')
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)