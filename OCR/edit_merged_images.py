import cv2 as cv
from OCR.img_methods import save_img
from OCR.tesseract_pressemappe import get_text_files_from_jpgs

img_1 = cv.imread('jpgs_sharpened/aktuelles_muster_5_3.jpg')
gray_1 = cv.cvtColor(img_1, cv.COLOR_BGR2GRAY)
print(gray_1.shape)
img_2 = cv.imread('jpgs_for_doku/aktuelle_konturen_erosion_2_2_closing_2_2_double.jpg')
gray_2 = cv.cvtColor(img_2, cv.COLOR_BGR2GRAY)
print(gray_2.shape)
dst = cv.bitwise_and(gray_1, gray_2)

# neg = cv.imread('jpgs_sharpened/contours_white_border_linetype_8_hierarchy_respected_fil_5_neg.jpg')
# gray_neg = cv.cvtColor(neg, cv.COLOR_BGR2GRAY)
# gray_neg_inverted = cv.bitwise_not(gray_neg)


# image3 = cv.bitwise_or(dst, gray_neg_inverted)
# für die kleinen Konturen hier noch ein bitwise-or einführen, sodass diese überschrieben werden!!!

# erosion = cv.dilate(dst,(2,2),iterations = 1)
# opening = cv.morphologyEx(dst, cv.MORPH_OPEN, (9,9)) # beides nicht sinnvoll.


save_img(dst, 'added_aktuelle_konturen_erosion_2_2_triple_closing_2_2_double.JPG', 'jpgs_sharpened/')
get_text_files_from_jpgs('jpgs_sharpened', ['added_aktuelle_konturen_erosion_2_2_triple_closing_2_2_double.JPG'])