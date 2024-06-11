from fastapi import APIRouter
import os

router  = APIRouter(
    prefix="/api/setupdirs",
    tags=["setup directories"]
)

@router.post("/setup-dirs")
async def setup_directories(new_folder_index=1):
    failed_images_count = 0

    dir_paths = {}
    
    uploaded_images_dir = os.path.join('API', 'uploaded_images')

    target_dir = f'new_label_data{new_folder_index}'
    sub_dirs = ['train', 'valid', 'test']
    data_dirs = ['images', 'labels']
    # sub_dirs = ['labels', 'images', 'failed_images']
    
    while os.path.exists(target_dir):
        new_folder_index += 1
        target_dir = f'new_label_data{new_folder_index}'

        dir_paths['target_dir'] = target_dir
    
    # 임시 테스트용 ###############################################
    original_images_dir = os.path.join(target_dir, 'images')
    os.makedirs(original_images_dir, exist_ok=True)
    original_labels_dir = os.path.join(target_dir, 'labels')
    os.makedirs(original_labels_dir, exist_ok=True)
    dir_paths['original_images_dir'] = original_images_dir
    dir_paths['original_labels_dir'] = original_labels_dir
    ############################################################

    for sub_dir in sub_dirs:
        dir_path = os.path.join(target_dir, sub_dir)
        dir_name = sub_dir
        os.makedirs(dir_path, exist_ok=True)

        dir_paths[dir_name] = os.path.abspath(dir_path)

        for data_dir in data_dirs:
            data_dir_path = os.path.join(dir_path, data_dir)
            data_dir_name = f'{sub_dir}_{data_dir}'
            os.makedirs(data_dir_path, exist_ok=True)

            dir_paths[data_dir_name] = os.path.abspath(data_dir_path)
    
    failed_images_dir = os.path.join(target_dir, 'failed_images')
    os.makedirs(failed_images_dir, exist_ok=True)
    dir_paths['failed_images_dir'] = failed_images_dir
        
    return dir_paths