import { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { Navigate } from "react-router-dom";

function AdminRoute({ children }) {
  const { user, loading } = useContext(AuthContext);

  if (loading) return <div>Loading...</div>;

  if (!user) {
    return <Navigate to="/" />;
  }

  return user.role === "admin" || user.role ==="superAdmin" ? children : <Navigate to="/Home" />;
}
export default AdminRoute