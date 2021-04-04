import sqlalchemy

print(sqlalchemy.__version__)

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean,ForeignKey

engine = create_engine('sqlite:///college.db', echo=True)

meta = MetaData()

filename = Table(
    'filename', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('path', String),
    Column('file_added', DateTime),
    Column('file_updated', DateTime),
    Column('scanned', Boolean),
    Column('file_meta_updated', DateTime),
)

text = Table(
    'text', meta,
    Column('id', Integer, primary_key=True),
    Column('file_id', Integer, ForeignKey('filename.id')),
    Column('text_data', String),
)
meta.create_all(engine)
