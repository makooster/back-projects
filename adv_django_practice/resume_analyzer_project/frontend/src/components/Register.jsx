import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const Register = () => {
    const [form, setForm] = useState({
        username: "",
        email: "",
        password: "",
        password2: "",
        first_name: "",
        last_name: "",
        role: "job_seeker",
    });
    const navigate = useNavigate();

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        await axios.post("/api/auth/register/", form);
        navigate("/login");
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 border rounded">
            <h1 className="text-2xl mb-4">Register</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input type="text" name="username" placeholder="Username" value={form.username} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="email" name="email" placeholder="Email" value={form.email} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="password" name="password" placeholder="Password" value={form.password} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="password" name="password2" placeholder="Confirm Password" value={form.password2} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="text" name="first_name" placeholder="First Name" value={form.first_name} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="text" name="last_name" placeholder="Last Name" value={form.last_name} onChange={handleChange} className="w-full p-2 border rounded" />
                <select name="role" value={form.role} onChange={handleChange} className="w-full p-2 border rounded">
                    <option value="job_seeker">Job Seeker</option>
                    <option value="recruiter">Recruiter</option>
                </select>
                <button type="submit" className="w-full bg-green-500 text-white p-2 rounded">
                    Register
                </button>
            </form>
        </div>
    );
};

export default Register;