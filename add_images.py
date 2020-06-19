import cv2 as cv


def saveimg(img, picture, output_path):
    try:
        cv.imwrite(output_path + picture, img)
    except:
        print('writing file failed', img)


img_1 = cv.imread('jpgs_sharpened/000010_000xx_00001_Laplacian.JPG')
img_2 = cv.imread('jpgs_sharpened/000010_000xx_00001_adaptiveThreshold_11_9_on_filtered.JPG')
img_2 = cv.bitwise_not(img_2)
dst = cv.add(img_1,img_2)
dst = cv.bitwise_not(dst)
saveimg(dst, 'added.JPG', 'jpgs_sharpened/')