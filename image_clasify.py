import os
from time import perf_counter
import re
import cv2
import easyocr
import matplotlib.pyplot as plt
from pprint import pprint
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime


def recognize_text(img_path):
    '''loads an image and recognizes text.'''
    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path,paragraph=True)


def display_file(file,data):
    img = cv2.imread(file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    dpi = 80
    fig_width, fig_height = int(img.shape[0] / dpi), int(img.shape[1] / dpi)
    plt.figure()
    f, axarr = plt.subplots(1, 2, figsize=(fig_width, fig_height))
    axarr[0].imshow(img)
    pprint(data)
    for (bbox, text, prob) in data:
        if prob >= 0.5:
            # display
            print(f'Detected text: {text} (Probability: {prob:.2f})')
            # get top-left and bottom-right bbox vertices
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = (int(top_left[0]), int(top_left[1]))
            bottom_right = (int(bottom_right[0]), int(bottom_right[1]))
            # create a rectangle for bbox display
            cv2.rectangle(img=img, pt1=top_left, pt2=bottom_right, color=(255, 0, 0), thickness=10)
            # put recognized text
            cv2.putText(img=img, text=text, org=(top_left[0], top_left[1] - 10), fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                        fontScale=1, color=(255, 0, 0), thickness=8)
    axarr[1].imshow(img)
    plt.show()


def get_files(dir_name):
    file_list = []
    for (dir_path, dir_names, dir_files) in os.walk(dir_name):
        file_list += [os.path.join(dir_path, cur_files)
                      for cur_files in dir_files

                      if re.search("[\w]+\.(?i)(jpe?g|png|gif|bmp)$", cur_files)]
    print(f"\n\n\nNumber of files {len(file_list)}")
    return file_list


def add_file_data(file, engine, filename, text):
    conn = engine.connect()
    print(f"Executing for file  {file} ")
    created = os.stat(file).st_mtime
    s = filename.select().where(filename.columns.path == file)
    result = conn.execute(s)
    file_result = result.fetchall()
    if len(file_result) == 0:
        print("file entry doesnot exists ")
        ins = filename.insert().values(name=os.path.basename(file),
                                       path=file,
                                       file_added=datetime.datetime.utcnow(),
                                       scanned=True,
                                       file_meta_updated=datetime.datetime.fromtimestamp(created))
        result = conn.execute(ins)
        id = result.inserted_primary_key
        data = recognize_text(file)
        for each in data:
            print(each)
            print(f'Detected text: {each[1]} (Probability: {88:.2f})')
            ins = text.insert().values(file_id=id[0],
                                       text_data=each[1],
                                       vector=str(each[0])
                                       )
            conn.execute(ins)
    else:
        return (f"Data already exists for  {file}")


def get_files_status(files, engine, filename):
    all_files_count = len(files)
    new_file = []
    synced_files = []
    conn = engine.connect()
    for file in files:
        s = filename.select().where(filename.columns.path == file)
        result = conn.execute(s)
        file_result = result.fetchall()
        if len(file_result) == 0:
            new_file.append(file)
        else:
            synced_files.append(file)
    print(f"Total number of files  {all_files_count}")
    print(f"number of synced files  {len(synced_files)}")
    print(f"number of new files  {len(new_file)}")


def update_to_db(files, engine, filename, text):
    for file in files:
        add_file_data(file, engine, filename, text)


def search_text(search_data, engine, filename, text):
    print(f"Searching for text {search_data}")
    conn = engine.connect()
    s = text.select().where(filename.columns.text_data.contains(search_data))
    result = conn.execute(s)
    file_result = result.fetchall()
    print(f"Number of file found  {len(file_result)}")



def main():
    print('Starting image processing ')
    files = get_files(r"S:\images\Screenshots")

    engine = create_engine('sqlite:///college.db')
    meta = MetaData()
    filename = Table(
        'filename', meta,
        Column('id', Integer, primary_key=True),
        Column('name', String),
        Column('path', String),
        Column('file_added', DateTime),
        Column('scanned', Boolean),
        Column('file_meta_updated', DateTime),
    )
    text = Table(
        'text', meta,
        Column('id', Integer, primary_key=True),
        Column('file_id', Integer, ForeignKey('filename.id')),
        Column('text_data', String),
        Column('vector', String),
    )
    get_files_status(files, engine, filename)

    # update to database
    update_to_db(files, engine, filename, text)

    search_data = "python"
    search_text(search_data, engine, filename, text)

if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
