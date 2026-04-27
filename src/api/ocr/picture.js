import request from "@/utils/request";

export function list(query) {
  return request({
    url: "/ocr/picture/allPage",
    method: "get",
    params: query
  });
}

export function addPicture(data) {
  return request({
    url: "/ocr/picture",
    method: "post",
    data: data
  });
}

export function deleteRow(id) {
  return request({
    url: "/ocr/picture/" + id,
    method: "delete"
  });
}
