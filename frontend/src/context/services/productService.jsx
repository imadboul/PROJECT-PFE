import api from "../../api/axios";
// GET
export const getProducts = () =>
  api.get("/catalog/product/");

export const getProductTypes = () =>
  api.get("/catalog/productType/");

// POST
export const createProduct = (data) =>
  api.post("/catalog/product/", data);

export const createProductType = (data) =>
  api.post("/catalog/productType/", data);

//  UPDATE
export const updateProduct = (id, data) => {
  return api.put("/catalog/product/", {
    id,
    ...data,
  });
};

export const updateProductType = (id, data) => {
  return api.put("/catalog/productType/", {
    id,
    ...data,
  });
};

//  DELETE
export const deleteProduct = (id) => {
  return api.delete("/catalog/product/", {
    data: { id },
  });
};

export const deleteProductType = (id) => {
  return api.delete("/catalog/productType/", {
    data: { id },
  });
};