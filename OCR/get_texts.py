from OCR.sharpen_images import sharpen_images_and_get_text_files
from OCR.merge_images import merge_pictures
from OCR.tesseract_pressemappe import get_text_files_from_jpgs
import os
from OCR.cut_articles_from_scans import cut_articles
from OCR.rotate_files_to_horizontal import determine_rotation_degree_and_rotate
from OCR.get_jpgs import get_jpg
from datetime import datetime
import ray
import sys


jpgs_names_for_evaluation = [ "0000xx/000010/000xx/00002/PIC/P000010000000000000000020000_0000_00000000HP_A.JPG",
                       "0000xx/000010/000xx/00002/PIC/P000010000000000000000020001_0000_00000000HP_A.JPG",
                       "0000xx/000010/000xx/00001/PIC/P000010000000000000000010000_0000_00000000HP_A.JPG",
                       "0000xx/000012/000xx/00001/PIC/P000012000000191479000010000_0000_00000000HP_A.JPG",
                       "0000xx/000034/001xx/00168/PIC/P000034000000000000001680000_0000_00000P34HP_A.JPG",
                       "0077xx/007779/000xx/00001/PIC/P007779000000191478000010000_0000_00000000HP_A.JPG",
                       "0112xx/011242/000xx/00011/PIC/P011242000000191477000110000_0000_00000000HP_A.JPG",
                       "0074xx/007478/000xx/00004/PIC/P007478000000000000000040000_0000_00000000HP_A.JPG",
                       "0425xx/042518/000xx/00052/PIC/P042518000000000000000520000_0000_00000000KP_A.JPG",
                       "0425xx/042518/000xx/00052/PIC/P042518000000000000000520001_0000_00000000KP_A.JPG",
                       "0109xx/010995/000xx/00004/PIC/P010995000000000000000040000_0000_00000M48HP_A.JPG",
                       "0423xx/042397/000xx/00002/PIC/P042397000000191477000020000_0000_00000000HP_A.JPG",
                       "0423xx/042397/000xx/00002/PIC/P042397000000191477000020001_0000_00000000HP_A.JPG",
                       "0423xx/042397/000xx/00002/PIC/P042397000000191477000020002_0000_00000000HP_A.JPG",
                       "0423xx/042397/000xx/00002/PIC/P042397000000191477000020003_0000_00000000HP_A.JPG",
                       "0036xx/003644/000xx/00004/PIC/P003644000000000000000040000_0000_00000000HP_A.JPG",
                       "0000xx/000010/000xx/00005/PIC/P000010000000000000000050000_0000_00000000HP_A.JPG",
                       "0000xx/000012/000xx/00005/PIC/P000012000000191477000050000_0000_00000000HP_A.JPG",
                       "0000xx/000012/000xx/00005/PIC/P000012000000191477000050001_0000_00000000HP_A.JPG",
                       "0036xx/003644/000xx/00003/PIC/P003644000000000000000030000_0000_00000000HP_A.JPG",
                       "0044xx/004455/000xx/00001/PIC/P004455000000191478000010000_0000_00000000HP_A.JPG",
                       "0000xx/000022/000xx/00040/PIC/P000022000000000000000400000_0000_00000X49HP_A.JPG",
                       "0000xx/000022/000xx/00015/PIC/P000022000000000000000150000_0000_00000000HP_A.JPG",
                       "0032xx/003281/000xx/00008/PIC/P003281000000000000000080000_0000_00000000HP_A.JPG",
                       "0032xx/003281/000xx/00005/PIC/P003281000000000000000050000_0000_00000000HP_A.JPG",
                       "0000xx/000010/000xx/00006/PIC/P000010000000191477000060000_0000_00000000HP_A.JPG",
                       "0000xx/000010/000xx/00006/PIC/P000010000000191477000060001_0000_00000000HP_A.JPG",
                       "0000xx/000012/000xx/00002/PIC/P000012000000191479000020000_0000_00000000HP_A.JPG",
                       "0000xx/000034/001xx/00162/PIC/P000034000000000000001620000_0000_00000P34HP_A.JPG",
                       "0099xx/009942/000xx/00003/PIC/P009942000000000000000030000_0000_00000000HP_A.JPG",
                       "0099xx/009942/000xx/00003/PIC/P009942000000000000000030001_0000_00000000HP_A.JPG",
                       "0032xx/003274/000xx/00052/PIC/P003274000000000000000520000_0000_00000000HP_A.JPG",
                       "0090xx/009021/000xx/00004/PIC/P009021000000000000000040000_0000_00000X48HP_A.JPG",
                       "0001xx/000135/000xx/00067/PIC/P000135000000000000000670000_0000_00000X48HP_A.JPG",
                       "0046xx/004600/000xx/00003/PIC/P004600000000191477000030000_0000_00000000HP_A.JPG",
                       "0110xx/011060/000xx/00010/PIC/P011060000000191477000100000_0000_00000000HP_A.JPG",
                       "0110xx/011060/000xx/00040/PIC/P011060000000000000000400000_0000_00000000HP_A.JPG"]


jpgs_for_evaluation = [ "0000xx_000010_000xx_00002_PIC_P000010000000000000000020000_0000_00000000HP_A.JPG",
                       "0000xx_000010_000xx_00002_PIC_P000010000000000000000020001_0000_00000000HP_A.JPG",
                       "0000xx_000010_000xx_00001_PIC_P000010000000000000000010000_0000_00000000HP_A.JPG",
                       "0000xx_000012_000xx_00001_PIC_P000012000000191479000010000_0000_00000000HP_A.JPG",
                       "0000xx_000034_001xx_00168_PIC_P000034000000000000001680000_0000_00000P34HP_A.JPG",
                       "0077xx_007779_000xx_00001_PIC_P007779000000191478000010000_0000_00000000HP_A.JPG",
                       "0112xx_011242_000xx_00011_PIC_P011242000000191477000110000_0000_00000000HP_A.JPG",
                       "0074xx_007478_000xx_00004_PIC_P007478000000000000000040000_0000_00000000HP_A.JPG",
                       "0425xx_042518_000xx_00052_PIC_P042518000000000000000520000_0000_00000000KP_A.JPG",
                       "0425xx_042518_000xx_00052_PIC_P042518000000000000000520001_0000_00000000KP_A.JPG",
                       "0109xx_010995_000xx_00004_PIC_P010995000000000000000040000_0000_00000M48HP_A.JPG",
                       "0423xx_042397_000xx_00002_PIC_P042397000000191477000020000_0000_00000000HP_A.JPG",
                       "0423xx_042397_000xx_00002_PIC_P042397000000191477000020001_0000_00000000HP_A.JPG",
                       "0423xx_042397_000xx_00002_PIC_P042397000000191477000020002_0000_00000000HP_A.JPG",
                       "0423xx_042397_000xx_00002_PIC_P042397000000191477000020003_0000_00000000HP_A.JPG",
                       "0036xx_003644_000xx_00004_PIC_P003644000000000000000040000_0000_00000000HP_A.JPG",
                       "0000xx_000010_000xx_00005_PIC_P000010000000000000000050000_0000_00000000HP_A.JPG",
                       "0000xx_000012_000xx_00005_PIC_P000012000000191477000050000_0000_00000000HP_A.JPG",
                       "0000xx_000012_000xx_00005_PIC_P000012000000191477000050001_0000_00000000HP_A.JPG",
                       "0036xx_003644_000xx_00003_PIC_P003644000000000000000030000_0000_00000000HP_A.JPG",
                       "0044xx_004455_000xx_00001_PIC_P004455000000191478000010000_0000_00000000HP_A.JPG",
                       "0000xx_000022_000xx_00040_PIC_P000022000000000000000400000_0000_00000X49HP_A.JPG",
                       "0000xx_000022_000xx_00015_PIC_P000022000000000000000150000_0000_00000000HP_A.JPG",
                       "0032xx_003281_000xx_00008_PIC_P003281000000000000000080000_0000_00000000HP_A.JPG",
                       "0032xx_003281_000xx_00005_PIC_P003281000000000000000050000_0000_00000000HP_A.JPG",
                       "0000xx_000010_000xx_00006_PIC_P000010000000191477000060000_0000_00000000HP_A.JPG",
                       "0000xx_000010_000xx_00006_PIC_P000010000000191477000060001_0000_00000000HP_A.JPG",
                       "0000xx_000012_000xx_00002_PIC_P000012000000191479000020000_0000_00000000HP_A.JPG",
                       "0000xx_000034_001xx_00162_PIC_P000034000000000000001620000_0000_00000P34HP_A.JPG",
                       "0099xx_009942_000xx_00003_PIC_P009942000000000000000030000_0000_00000000HP_A.JPG",
                       "0099xx_009942_000xx_00003_PIC_P009942000000000000000030001_0000_00000000HP_A.JPG",
                       "0032xx_003274_000xx_00052_PIC_P003274000000000000000520000_0000_00000000HP_A.JPG",
                       "0090xx_009021_000xx_00004_PIC_P009021000000000000000040000_0000_00000X48HP_A.JPG",
                       "0001xx_000135_000xx_00067_PIC_P000135000000000000000670000_0000_00000X48HP_A.JPG",
                       "0046xx_004600_000xx_00003_PIC_P004600000000191477000030000_0000_00000000HP_A.JPG",
                       "0110xx_011060_000xx_00010_PIC_P011060000000191477000100000_0000_00000000HP_A.JPG",
                       "0110xx_011060_000xx_00040_PIC_P011060000000000000000400000_0000_00000000HP_A.JPG"]

ray.init()

@ray.remote
# Klasse für die spätere Verwendung als Actor zum Sammeln der Artikel
class Article(object):
   # Initialisierung der Klasse
   def __init__(self, jpg_name, tess_path: str, source_dir_path: str = 'OCR/jpgs_cut',
                target_dir_path: str = 'OCR/pressemappe_text_files'):
       self.image = jpg_name
       self.tess_path = tess_path
       self.source_dir_path = source_dir_path
       self.target_dir_path = target_dir_path
       self.text = ''

   # Funktion zum Scrapen der Ratings
   def get_text(self):
       try:
           picture = self.image
           start = datetime.now()
           if picture not in os.listdir(self.source_dir_path):
               cut_articles([picture])
           sharpened = sharpen_images_and_get_text_files([picture], source_directory='OCR/jpgs_cut',
                                                         do_save_img=True)[0]
           merged = merge_pictures(picture, do_save_img=False, gray_1=sharpened, img_obj_given=True)
           rotated = determine_rotation_degree_and_rotate(picture, do_save_img=False)
           try:
               text_sharpened = get_text_files_from_jpgs([picture], tesseract_dir_path=self.tess_path, img_obj=sharpened,
                                                     save_file=False, img_obj_given=True)
           except Exception as e:
               print(e)
               text_sharpened = ''
           try:
               text_merged = get_text_files_from_jpgs([picture], tesseract_dir_path=self.tess_path, img_obj=merged,
                                                      save_file=False, img_obj_given=True)
           except Exception as e:
               print(e)
               text_merged = ''
           try:
               text_rotated = get_text_files_from_jpgs([picture], tesseract_dir_path=self.tess_path, img_obj=rotated,
                                                   save_file=False, img_obj_given=True)
           except Exception as e:
               print(e)
               text_rotated = ''
           txt_name = picture.replace('.JPG', '')
           text = text_sharpened + '\n' + text_merged + '\n' + text_rotated
           text = text.encode('utf-8')
           text = text.decode('utf-8')
           time_difference = (datetime.now() - start).total_seconds()
           print(time_difference)
           picture = picture[:57] + '0'
           if picture in os.listdir(self.target_dir_path):
               with open(self.target_dir_path + '/' + picture, 'a', encoding='utf-8') as text_file:
                   print(picture)
                   text_file.write(text)
           else:
               with open(self.target_dir_path + '/' + picture, 'w', encoding='utf-8') as text_file:
                   print(picture)
                   text_file.write(text)
           self.text = text
       except Exception as e:
           exc_type, exc_obj, exc_tb = sys.exc_info()
           fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
           print()
           print('Error! Code: {c}, Message, {m}, Type, {t}, File, {f}, Line {line}'.format(c=type(e).__name__, m=str(e), t=exc_type, f=fname, line=exc_tb.tb_lineno))

   def read(self):
       return self.text


def get_texts(jpg_list, tesseract_path, source_dir_path, target_dir_path):
   print(jpg_list, tesseract_path, source_dir_path, target_dir_path)
   print(len(jpg_list))
   for index in range(0, len(jpg_list)-1, 5):
       if index > (len(jpg_list) - 5):
           article_actors = \
               [Article.remote(jpg_list[index:], tesseract_path, source_dir_path, target_dir_path) for i in range(5)]
           [a.get_text.remote() for a in article_actors]
           texts = [a.read.remote() for a in article_actors]
           ray.get(texts)
       else:
           article_actors = \
               [Article.remote(jpg_list[index + i], tesseract_path, source_dir_path, target_dir_path) for i in range(5)]
           [a.get_text.remote() for a in article_actors]
           texts = [a.read.remote() for a in article_actors]
           ray.get(texts)


if __name__ == '__main__':
   jpg_list = ['http://webopac.hwwa.de/DigiPerson/P/' + jpg for jpg in jpgs_names_for_evaluation]
   for jpg in jpg_list:
       get_jpg(jpg)
   tess_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   get_texts(jpgs_for_evaluation, tesseract_path=tess_path,
                   source_dir_path='OCR/jpgs', target_dir_path='OCR/pressemappe_text_files')
