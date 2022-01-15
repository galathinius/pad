import axios from "axios";

export const get_text = (id: any) => {
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
