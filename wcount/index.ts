import { get_text } from "./services";
import express from "express";
import cors from "cors";
// const { text } = require("express");

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

app.get("/api/count/:id", (request, response) => {
  const id: any = String(request.params.id);
  console.log("got req for " + id);
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
