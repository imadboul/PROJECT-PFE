import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getProductTypes, createProduct } from "../context/services/productService";
import { Controller, useForm } from "react-hook-form";
import Select from "react-select";
import { NavLink } from "react-router-dom";

function AddProduct() {
  const [productTypes, setProductTypes] = useState([]);
  const [loading, setLoading] = useState(false);

  const {
    register,
    handleSubmit,
    reset,
    control,
    watch,
    formState: { errors },
  } = useForm();

  const options = productTypes.map(type => ({
    value: type.id,
    label: type.name
  }));

  const selectedType = watch("productType");

  // Fetch product types
  useEffect(() => {
    const fetchProductTypes = async () => {
      try {
        const res = await getProductTypes();
        const data = res.data.types || res.data;
        setProductTypes(Array.isArray(data) ? data : []);
      } catch (err) {
        toast.error("Error fetching product types", err);
      }
    };

    fetchProductTypes();
  }, []);

  const onSubmit = async (data) => {
    try {
      setLoading(true);

      const payload = {
        name: data.name,
        description: data.description,
        unit_price: Number(data.unitPrice),
        qte_left: Number(data.qteLeft),
        product_type: Number(data.productType),
      };

      await createProduct(payload);

      toast.success("Product created successfully");
      reset();

    } catch (error) {
      const msg =
        error.response?.data?.error
          ? JSON.stringify(error.response.data.error)
          : error.response?.data?.detail ||
          JSON.stringify(error.response?.data) ||
          "Error creating product";

      toast.error(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-transparent text-white">
      <div className="w-full max-w-xl bg-black/60 rounded-2xl shadow-lg p-6 border border-black/60">

        <h2 className="text-2xl font-bold text-center mb-6 text-orange-500">
          Add Product
        </h2>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">

          {/* Name */}
          <input
            type="text"
            placeholder="Name"
            {...register("name", { required: "Name is required" })}
            className="w-full text-xl p-2 border border-black rounded"
          />
          {errors.name && (
            <p className="text-red-500 text-xs text-center">
              {errors.name.message}
            </p>
          )}

          {/* Description */}
          <textarea
            placeholder="Description"
            {...register("description")}
            className="w-full text-xl p-2 border border-black rounded"
          />

          {/* Unit Price */}
          <input
            type="number"
            placeholder="Unit Price"
            {...register("unitPrice", {
              required: "Unit price is required",
              min: { value: 1, message: "Must be > 0" },
            })}
            className="w-full text-xl p-2 border border-black rounded"
          />
          {errors.unitPrice && (
            <p className="text-red-500 text-xs text-center">
              {errors.unitPrice.message}
            </p>
          )}

          {/* Quantity */}
          <input
            type="number"
            placeholder="Quantity Left"
            {...register("qteLeft", {
              required: "Quantity is required",
              min: { value: 1, message: "Must be > 0" },
            })}
            className="w-full text-xl p-2 border border-black rounded"
          />
          {errors.qteLeft && (
            <p className="text-red-500 text-xs text-center">
              {errors.qteLeft.message}
            </p>
          )}

          {/* Product Type */}
          <div className="flex items-center gap-4">
            {/* Product Type */}
            <Controller
              name="productType"
              control={control}
              rules={{ required: "Product type is required" }}
              render={({ field }) => (
                <Select
                  {...field}
                  options={options}
                  placeholder="Select Product Type"
                  styles={{
                    control: (base, state) => ({
                      ...base,
                      backgroundColor: "rgba(7, 7, 7, 0.11)",
                      borderColor: state.isFocused ? "#f97316" : "#000",
                      boxShadow: "none",
                      fontSize: "20px",
                      "&:hover": {
                        border: "1px solid #f97316"
                      }
                    }),

                    menu: (base) => ({
                      ...base,
                      backgroundColor: "rgba(0, 0, 0, 0.66)"
                    }),

                    option: (base, state) => ({
                      ...base,
                      backgroundColor: state.isFocused
                        ? "rgba(247, 77, 9, 0.96)"
                        : "rgba(0, 0, 0, 0.66)",
                      color: "#fff",
                      cursor: "pointer",
                      fontSize: "20px",
                      fontWeight: "400",
                      border: "1px solid #000",
                      "&:active": {
                        backgroundColor: "#f97316"
                      }
                    }),

                    singleValue: (base) => ({
                      ...base,
                      color: "#fff",
                    }),

                    placeholder: (base) => ({
                      ...base,
                      color: "#fff",

                    })
                  }}
                  onChange={(selected) => field.onChange(selected.value)}
                  value={options.find(opt => opt.value === field.value)}
                />
              )}
            />

            {/* Add Type */}
            <NavLink to="/AddProductType" className="text-orange-400 text-xl">
              <i className="fa-solid fa-plus"></i>
            </NavLink>

            {/* Edit Type */}
            <NavLink
              to={
                selectedType
                  ? `/EditProductType/${selectedType}`
                  : "#"
              }
              onClick={(e) => {
                if (!selectedType) {
                  e.preventDefault();
                  toast.error("Select a product type first");
                }
              }}
              className="text-orange-400 text-xl"
            >
              <i className="fa-solid fa-pen"></i>
            </NavLink>
          </div>

          {errors.productType && (
            <p className="text-red-500 text-xs text-center">
              {errors.productType.message}
            </p>
          )}

          {/* Submit */}
          <button
            type="submit"
            disabled={loading}
            className="w-full py-2 font-bold bg-orange-600 hover:bg-orange-700 rounded text-white"
          >
            {loading ? "Loading..." : "Create Product"}
          </button>

        </form>
      </div>
    </div>
  );
}

export default AddProduct;