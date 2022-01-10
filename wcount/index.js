const express = require("express");
const axios = require("axios");
const cors = require("cors");
const { text } = require("express");

const app = express();
const port = 3000;
const host = "0.0.0.0";
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.listen(port, host, () => {
  console.log(`Example app listening at http://localhost:${port}`);
});

let get_text = (id) => {
  const request = axios.get("http://distributor:8000/items/" + id);
  // .then(function (response) {
  //   // handle success
  //   //   let text =;

  //   console.log(response.data.text);
  //   return response.data.text;
  // })
  // .catch(function (error) {
  //   // handle error
  //   console.log(error);
  // })
  // .then(function () {
  //   // always executed
  // });
  return request.then(function (response) {
    return response.data.text;
  });
};

app.get("/api/count/:id", (request, response) => {
  const id = String(request.params.id);
  get_text(id).then((text) => {
    let count = text.trim().split(/\s+/).length;
    let to_send = {
      id: id,
      text: text,
      word_count: count,
    };
    response.json(to_send);
  });
});
