from fastapi import FastAPI
from type_models import Text, TextId
from mongo_funcs import get_data, send_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: str):

    text = get_data(item_id)
    # items.append(text)
    return Text(text=text)


@app.post("/items/")
async def create_item(item: Text):
    uid = send_data(item.dict()['text'])
    return TextId(text_id=uid)
