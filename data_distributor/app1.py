from flask import Flask
from flask_pymongo import PyMongo


# pip freeze > requirements.txt


app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://root:pass12345@mongo1:27017"
mongo = PyMongo(app)

# if __name__ == '__main__':
#       app.run(host='0.0.0.0', port=8000)

if 'foo' not in mongo.database_names():
    # create db foo
    pass


@app.route('/')
def hello_world():
    return 'Hello, Docker!'
