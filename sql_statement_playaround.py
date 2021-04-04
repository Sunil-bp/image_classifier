from sqlalchemy import create_engine, MetaData,and_, Table, Column, Integer, String, DateTime, Boolean, ForeignKey

engine = create_engine('sqlite:///college.db', echo=True)

conn = engine.connect()

print(engine.table_names())

wait = input("wait ")
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

# ins = filename.insert().values(name='Ravi')
# print(str(ins))
# result = conn.execute(ins)
# print(result)



s = filename.select().where(filename.columns.path=='Ravi')
print(str(s))
print(s.compile().params)
result = conn.execute(s)
print(len(result.fetchall()))
for row in result:
    print(row)