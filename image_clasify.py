import os
from time import perf_counter
import re
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt


def recognize_text(img_path):
    '''loads an image and recognizes text.'''

    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path,paragraph=False)

def get_files(dir_name):
    file_list  = []
    for (dir_path, dir_names, dir_files) in os.walk(dir_name):
        file_list += [os.path.join(dir_path,cur_files)
                      for cur_files in dir_files
                      if re.search("[\w]+\.(?i)(jpe?g|png|gif|bmp)$",cur_files)]
    print(f"\n\n\nNumber of files {len(file_list)}")
    return file_list

def main():
    print('Starting image processing ')
    print("Getting all image files  ")
    files = get_files(r"C:\Users\sunil\Desktop\meme_classifier\test_data")
    final_data  = { }
    for file  in files:
        print(f"executing for file  {file} ")
        data  = recognize_text(file)
        print(data)
        ait  = input("hello")


if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)