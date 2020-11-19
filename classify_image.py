try:
    from PIL import Image
except ImportError:
    import Image
import os,re
import pytesseract
from time import perf_counter

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
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    if os.path.exists(r'S:\IAMGE BACK\Screenshots\Screenshot_2020-01-02-22-28-41-424_com.tinder.jpg'):
        print("File is reachable ")
    print(pytesseract.image_to_string(Image.open(r'S:\IAMGE BACK\Screenshots\Screenshot_2020-02-04-15-11-02-661_com.google.android.youtube.jpg')))

def main():
    print('Starting image processing ')
    print("Getting all image files  ")
    files = get_files(r"S:\\")
    # print(*files,sep="\n")

if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
