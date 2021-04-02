try:
    from PIL import Image
except ImportError:
    import Image
import cv2
import os,re
import pytesseract
import traceback
from time import perf_counter
import random
from pprint import pprint
##Get file list

def get_files(dir_name):
    file_list  = []
    for (dir_path, dir_names, dir_files) in os.walk(dir_name):
        file_list += [os.path.join(dir_path,cur_files)
                      for cur_files in dir_files
                      if re.search("[\w]+\.(?i)(jpe?g|png|gif|bmp)$",cur_files)]
    print(f"Number of files {len(file_list)}")
    return file_list


def get_image_data(file):
    if os.path.exists(file):
        print("File is reachable ")
    try:
        data  = pytesseract.image_to_string(Image.open(file))
        print("Data from image ")
        print(data)
    except:
        traceback.print_exc()


def get_image_data_cv(file):
    if os.path.exists(file):
        print("File is reachable ")
    try:
        image = cv2.imread(file)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        # custom_config = r'--oem 3 --psm 6'
        details = pytesseract.image_to_string(threshold_img, lang='eng')
        print(details.split())
        # cv2.imshow('image', image)
        # cv2.imshow('threshold image', threshold_img)

        # cv2.waitKey(0)
        cv2.destroyAllWindows()
        print("Data from image ")
        # print(data)
        return details.split()
    except:
        traceback.print_exc()

def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    print('Starting image processing ')
    print("Getting all image files  ")
    files = get_files(r"C:\Users\sunil\Desktop\meme_classifier\test_data")
    final_data  = { }
    for _  in files[0:25]:
        rand  = random.randint(0,len(files))
        print(f"executing for file  {files[rand]} ")
        final_data[files[rand]]  = get_image_data_cv(files[rand])
        # wait  = input("check data  ")
    import json
    with open('data.json', 'w') as outfile:
        json.dump(final_data, outfile)
    # print(*files,sep="\n")
    # pprint(final_data)


if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
