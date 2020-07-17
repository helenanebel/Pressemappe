from OCR.sharpen_images import sharpen_images_and_get_text_files
from OCR.merge_images import merge_pictures
from OCR.tesseract_pressemappe import get_text_files_from_jpgs

def get_texts(jpgs_list: list, source_dir_path: str = 'jpgs_cut', target_dir_path: str = 'pressemappe_text_files'):
    for picture in jpgs_list:
        sharpened = sharpen_images_and_get_text_files([picture], source_directory=source_dir_path,
                                          do_save_img=False)[0]
        merged = merge_pictures(picture, do_save_img=False)
        text_sharpened = get_text_files_from_jpgs([picture], img_obj=sharpened, save_file=False, img_obj_given=True)
        print('sharpened')
        text_merged = get_text_files_from_jpgs([picture], img_obj=merged, save_file=False, img_obj_given=True)
        print('merged')
        txt_name = picture.replace('.JPG', '')
        with open(target_dir_path + '/' + txt_name, 'w') as text_file:
            print(picture)
            text_file.write(text_sharpened + '\n' + text_merged)


if __name__ == '__main__':
    get_texts(['0000xx_000012_000xx_00001_PIC_P000012000000191479000010000_0000_00000000HP_A.JPG'])
