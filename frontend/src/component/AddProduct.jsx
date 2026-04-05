import { useEffect, useState } from "react";
import toast from "react-hot-toast";
import { getProductTypes, createProduct } from "../context/services/productService";
import { useForm } from "react-hook-form";
import { NavLink } from "react-router";

function AddProduct() {
    const [productTypes, setProductTypes] = useState([]);
    const [loading, setLoading] = useState(false);

    const {
        register,
        handleSubmit,
        reset,
        formState: { errors },
    } = useForm();

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
                        {...register("name", {
                            required: "Name is required",
                        })}
                        className="w-full text-xl placeholder-white text-white p-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
                    />
                    <div className="relative bottom-3">
                        {errors.name && (
                            <p className="absolute top-0 left-0 right-0 text-red-500 text-xs text-center mt-1">
                                {errors.name.message}
                            </p>
                        )}
                    </div>

                    {/* Description */}
                    <textarea
                        placeholder="Description"
                        {...register("description")}
                        className="w-full text-xl placeholder-white text-white p-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
                    />

                    {/* Unit Price */}
                    <input
                        type="number"
                        placeholder="Unit Price"
                        {...register("unitPrice", {
                            required: "Unit price is required",
                            min: { value: 1, message: "Must be greater than 0" },
                        })}
                        className="w-full text-xl placeholder-white text-white p-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
                    />
                    <div className="relative bottom-3">
                        {errors.unitPrice && (
                            <p className="absolute top-0 left-0 right-0 text-red-500 text-xs text-center mt-1">
                                {errors.unitPrice.message}
                            </p>
                        )}
                    </div>

                    {/* Quantity */}
                    <input
                        type="number"
                        placeholder="Quantity Left"
                        {...register("qteLeft", {
                            required: "Quantity is required",
                            min: { value: 1, message: "Must be greater than 0" },
                        })}
                        className="w-full text-xl placeholder-white text-white p-2 border border-black rounded focus:outline-none focus:ring-2 focus:ring-orange-500"
                    />
                    <div className="relative bottom-3">
                        {errors.qteLeft && (
                            <p className="absolute top-0 left-0 right-0 text-red-500 text-xs text-center mt-1">
                                {errors.qteLeft.message}
                            </p>
                        )}
                    </div>

                    {/* Product Type */}
                    <div className="flex justify-center items-center gap-4">
                    <select
                        {...register("productType", {
                            required: "Product type is required",
                        })}
                        className="w-full text-xl p-2 text-white border border-black rounded focus:outline-none focus:ring-2 focus:ring-orange-500 focus:text-black"
                    >
                        <option value="">Select Product Type</option>

                        {productTypes.map((type) => (
                            <option key={type.id} value={type.id}>
                                {type.name}
                            </option>
                        ))}
                    </select>
                    <NavLink
                        to="/AddProductType"
                        className="text-orange-400 px-4 py-2 text-xl hover:text-orange-600 transition">
                        <i className="fa-solid fa-plus"></i>
                    </NavLink>
                    <NavLink
                        to="/EditProductType"
                        className="text-orange-400 px-4 py-2 text-xl hover:text-orange-600 transition">
                        <i className="fa-solid fa-pen"></i>
                    </NavLink>
                    </div>

                    <div className="relative bottom-3">
                        {errors.productType && (
                            <p className="absolute top-0 left-0 right-0 text-red-500 text-xs text-center mt-1">
                                {errors.productType.message}
                            </p>
                        )}
                    </div>

                    {/* Submit */}
                    <button
                        type="submit"
                        disabled={loading}
                        className={`w-full mt-4 py-2 rounded-lg text-white transition
            ${loading
                                ? "bg-gray-500 cursor-not-allowed"
                                : "bg-gradient-to-br from-black to-orange-500 hover:to-orange-700"
                            }`}
                    >
                        {loading ? "Loading..." : "Create Product"}
                    </button>

                </form>
            </div>
        </div>
    );
}

export default AddProduct;