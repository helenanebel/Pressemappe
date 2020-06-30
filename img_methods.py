import cv2 as cv


def save_img(img, img_name, output_path):
    try:
        cv.imwrite(output_path + img_name, img)
    except Exception as e:
        print(e)
        print('writing file failed', img_name)


def color_to_gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)