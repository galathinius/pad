from uuid import uuid4
from itertools import cycle
from fastapi import FastAPI
from pymongo import MongoClient

from pydantic import BaseModel

MONGO_USER = 'root'
MONGO_PASS = 'pass12345'
DATA_MONGOS = ['mongo1', 'mongo2', 'mongo3']


app = FastAPI()
clients = [MongoClient(
    f'mongodb://{MONGO_USER}:{MONGO_PASS}@{m}:27017') for m in DATA_MONGOS]
dbs = [client.chunks.chunks for client in clients]
#              db     collection (table)
MONGO_POOL = cycle(dbs)


class Text(BaseModel):
    text: str


class Chunk(BaseModel):
    chunk: str
    text_id: str
    chunk_idx: int


class TextId(BaseModel):
    text_id: str


def chunks(lst, n):
    # Yield successive n-sized chunks from lst
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def send_data(a_text):
    uid = str(uuid4())
    idx = 0
    for part in chunks(a_text, 10):
        # create chunk obj
        new_item = {}
        new_item['chunk'] = part
        new_item['text_id'] = uid
        new_item['chunk_idx'] = idx
        idx += 1
        # get mongo conn
        conn = next(MONGO_POOL)
        # send to mongo
        conn.insert_one(new_item)

    return uid


def get_data(uid):
    data = []
    for db in dbs:
        items = db.find({"text_id": uid})
        data.extend(items)
    data = [Chunk(**i) for i in data]
    return data


def combine_chunks(chunks):
    chunk_list = [None] * len(chunks)
    for chunk in chunks:
        chunk_list[chunk.chunk_idx] = chunk.chunk
    the_text = ''.join(chunk_list)
    return the_text


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):
    items = get_data(item_id)
    text = combine_chunks(items)
    # items.append(text)
    return Text(text=text)


@app.post("/items/")
async def create_item(item: Text):
    uid = send_data(item.dict()['text'])
    return TextId(text_id=uid)
