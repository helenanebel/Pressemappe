import cv2 as cv


def saveimg(img, picture, output_path):
    try:
        cv.imwrite(output_path + picture, img)
    except:
        print('writing file failed', img)


img_1 = cv.imread('jpgs_sharpened/lap_edited_white_contours.jpg')
gray_1 = cv.cvtColor(img_1, cv.COLOR_BGR2GRAY)
print(gray_1.shape)
img_2 = cv.imread('pressemappe_results/test_5.JPG')
img_2 = img_2[:, 1:-1]
gray_2 = cv.cvtColor(img_2, cv.COLOR_BGR2GRAY)
print(gray_2.shape)
dst = cv.bitwise_and(gray_1, gray_2)

opening = cv.morphologyEx(dst, cv.MORPH_OPEN, (9,9))
opening = cv.morphologyEx(opening, cv.MORPH_OPEN, (9,9))
opening = cv.morphologyEx(opening, cv.MORPH_OPEN, (7,7))

saveimg(opening, 'opening.JPG', 'jpgs_sharpened/')