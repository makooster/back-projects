import { useState } from "react";
import { useAuth } from "../context/AuthContext";

const Login = () => {
    const { login } = useAuth();
    const [form, setForm] = useState({ username: "", password: "" });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await login(form);
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 border rounded">
            <h1 className="text-2xl mb-4">Login</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input
                    type="text"
                    name="username"
                    placeholder="Username"
                    value={form.username}
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                />
                <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    value={form.password}
                    onChange={handleChange}
                    className="w-full p-2 border rounded"
                />
                <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
                    Login
                </button>
            </form>
        </div>
    );
};

export default Login;
