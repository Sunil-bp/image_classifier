import os
from time import perf_counter
import re
import cv2
import numpy as np
import easyocr
import matplotlib.pyplot as plt
from pprint import pprint
from sqlalchemy import create_engine, MetaData,and_, Table, Column, Integer, String, DateTime, Boolean, ForeignKey
import datetime

def recognize_text(img_path):
    '''loads an image and recognizes text.'''

    reader = easyocr.Reader(['en'])
    return reader.readtext(img_path, paragraph=True)


def get_files(dir_name):
    file_list = []
    for (dir_path, dir_names, dir_files) in os.walk(dir_name):
        file_list += [os.path.join(dir_path, cur_files)
                      for cur_files in dir_files

                      if re.search("[\w]+\.(?i)(jpe?g|png|gif|bmp)$", cur_files)]
    print(f"\n\n\nNumber of files {len(file_list)}")
    return file_list

def add_file_data(file,conn,filename,text):
    print(f"Executing for file  {file} ")
    print(os.path.basename(file))
    created = os.stat(file).st_mtime
    print(f"file created date {datetime.datetime.fromtimestamp(created)}")
    s = filename.select().where(filename.columns.path == file)
    result = conn.execute(s)
    file_result = result.fetchall()
    print(f"len of file table results {len(file_result)}")
    if len(file_result) == 0:
        print("file entry doesnot exists ")
        ins = filename.insert().values(name=os.path.basename(file),
                                       path=file,
                                       file_added=datetime.datetime.utcnow(),
                                       scanned=True,
                                       file_meta_updated=datetime.datetime.fromtimestamp(created))
        print(str(ins))
        print(ins.compile().params)
        result = conn.execute(ins)
        id = result.inserted_primary_key
        data = recognize_text(file)

        # pprint(data)
        for each in data:
            ##add to text
            print(f"data is {each[1]}")
            print(f"file id is {id[0]}")
            ins = text.insert().values(file_id=id[0],
                                       text_data=each[1],
                                       vector=str(each[0])
                                       )
            print(str(ins))
            print(ins.compile().params)
            conn.execute(ins)
        ##scan and add to text data
    else:
        print("data already exists  ")

def main():
    print('Starting image processing ')
    print("Getting all image files  ")
    files = get_files(r"C:\Users\sunil\Desktop\meme_classifier\test_data")

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
    conn = engine.connect()

    for file in files:
        add_file_data(file,conn,filename,text)


if __name__ == '__main__':
    t1_start = perf_counter()
    main()
    t1_stop = perf_counter()
    print("Elapsed time:", t1_stop, t1_start)
    print("Elapsed time during the whole program in seconds:",
          t1_stop - t1_start)
