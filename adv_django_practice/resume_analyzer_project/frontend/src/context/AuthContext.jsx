import { createContext, useContext, useEffect, useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const navigate = useNavigate();

    useEffect(() => {
        const token = localStorage.getItem("token");
        if (token) {
            axios.get("/api/auth/me/", { headers: { Authorization: `Bearer ${token}` } })
                .then(res => setUser(res.data))
                .catch(() => logout());
        }
        setLoading(false);
    }, []);

    const login = async (data) => {
        const res = await axios.post("/api/auth/token/", data);
        localStorage.setItem("token", res.data.access);
        navigate("/");
    };

    const logout = () => {
        localStorage.removeItem("token");
        setUser(null);
        navigate("/login");
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
