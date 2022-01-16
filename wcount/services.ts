import axios from "axios";
import redis from "redis";

import { createClient } from "redis";

const client = createClient({
  url: "redis://cache:6379",
});
client.on("error", (err) => console.log("Redis Client Error", err));

export const get_text = async (id: any) => {
  await client.connect();
  const value = await client.get(id);
  if (value) {
    console.log("got response from cache " + value);
    return value;
  } else {
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
      const text = response.data.text;
      client.set(id, text);
      return text;
    });
  }
};
