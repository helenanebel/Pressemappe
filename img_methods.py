import cv2 as cv


def save_img(img, img_name, output_path):
    try:
        cv.imwrite(output_path + img_name, img)
    except Exception as e:
        print(e)
        print('writing file failed', img_name)


def color_to_gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


def rotate_by_degree(img, angle):
    return cv.warpAffine(img, cv.getRotationMatrix2D((img.shape[1]/2, img.shape[0]/2), angle, 1.0), (img.shape[1], img.shape[0]), borderValue=255)


