import os
from typing import List, Dict


import pandas as pd
from tqdm import tqdm
import nibabel as nib
from nilearn import plotting
import matplotlib.pyplot as plt

ROOT_DATASET_FOLDER = './data'

def process_folders(paths: List[str]):
    """Iterating over each folder:
        - rename original and segmented images
        - collect original and segmented images paths
        - count faild folders paths, where:
            faild folders <- missing one of [original | segmented] images

    Returns:
        rows List[Dict]: Original and Segmented images paths
        failed_folders: paths of folder whcih misses one of [original | segmented] images
    """

    rows, failed_folders = [], []
    for folder_index, folder in enumerate(tqdm(folders)):
        patient_folder_path = os.path.join(annotated_data_path, folder)
        content = os.listdir(patient_folder_path)

        if len(content) < 2:
            failed_folders.append(patient_folder_path)
            continue

        old_image_name, old_segmentation_name = content[0], content[1] # old images names
        new_image_name, new_segmentation_name = f'original_image_{folder_index}.nii', f'segmented_image_{folder_index}.nrrd'

        os.rename(f'{patient_folder_path}/{old_image_name}', f'{patient_folder_path}/{new_image_name}')
        os.rename (f'{patient_folder_path}/{old_segmentation_name}', f'{patient_folder_path}/{new_segmentation_name}')

        rows.append(
            {
                'Original Image path': f'{patient_folder_path}/{new_image_name}',
                'Segmented Image path': f'{patient_folder_path}/{new_segmentation_name}'
            }
        )
    return rows, failed_folders


def plot_nii_image(image_path: str):
    Nifti_img  = nib.load(image_path)
    nii_data = Nifti_img.get_fdata()
    nii_aff  = Nifti_img.affine
    nii_hdr  = Nifti_img.header
    print(nii_aff ,'\n',nii_hdr)
    print(nii_data.shape)
    if(len(nii_data.shape)==3):
        for slice_Number in range(nii_data.shape[2]):
            plt.imshow(nii_data[:,:,slice_Number ])
            plt.show()
    if(len(nii_data.shape)==4):
        for frame in range(nii_data.shape[3]):
            for slice_Number in range(nii_data.shape[2]):
                plt.imshow(nii_data[:,:,slice_Number,frame])
                plt.show()

# original images <- .nii extencion
data = pd.read_csv('patient_images.csv')
original_images = data['Original Image path'].values

path = original_images[1]



# if __name__ == "__main__":
#     annotated_data_path = f'{ROOT_DATASET_FOLDER}/annotated_data/slicer'
#     folders = sorted (os.listdir (annotated_data_path))
#
#     # rows, failed_folders = process_folders(paths = folders)
#     # print('Failed folders: ', failed_folders)
#     # df = pd.DataFrame(rows)
#     # df.to_csv ('patient_images.csv')
#
#     data = pd.read_csv('patient_images.csv')


