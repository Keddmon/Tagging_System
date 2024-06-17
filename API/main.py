from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

# Router
from domain.upload import upload_router
from domain.setup_directories import setup_directories
from domain.copy_images import copy_images
from domain.class_labeling import class_labeling
from domain.label_data import label_data
from domain.make_json import make_json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(upload_router.router)
app.include_router(setup_directories.router)
app.include_router(copy_images.router)
app.include_router(class_labeling.router)
app.include_router(label_data.router)
app.include_router(make_json.router)