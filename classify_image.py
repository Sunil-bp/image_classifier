try:
    from PIL import Image
except ImportError:
    import Image
import os,re
import pytesseract
import traceback
from time import perf_counter
import random

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


def main():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    print('Starting image processing ')
    print("Getting all image files  ")
    files = get_files(r"S:\IAMGE BACK\Screenshots")
    for _  in files:
        rand  = random.randint(0,len(files))
        print(f"executing for file  {files[rand]} ")
        get_image_data(files[rand])
        wait  = input("check data  ")

    # print(*files,sep="\n")

if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
