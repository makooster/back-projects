import { useState } from "react";
import axios from "axios";

const JobPost = () => {
    const [form, setForm] = useState({
        title: "",
        description: "",
        required_skills: "",
        location: "",
        salary: "",
    });

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const token = localStorage.getItem("token");
        await axios.post("/api/jobs/jobs/", {
            ...form,
            required_skills: form.required_skills.split(",").map(skill => skill.trim()),
        }, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });
        alert("Job posted!");
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 border rounded">
            <h1 className="text-2xl mb-4">Post a Job</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input type="text" name="title" placeholder="Job Title" value={form.title} onChange={handleChange} className="w-full p-2 border rounded" />
                <textarea name="description" placeholder="Job Description" value={form.description} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="text" name="required_skills" placeholder="Required Skills (comma separated)" value={form.required_skills} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="text" name="location" placeholder="Location" value={form.location} onChange={handleChange} className="w-full p-2 border rounded" />
                <input type="text" name="salary" placeholder="Salary" value={form.salary} onChange={handleChange} className="w-full p-2 border rounded" />
                <button type="submit" className="w-full bg-green-500 text-white p-2 rounded">
                    Post Job
                </button>
            </form>
        </div>
    );
};

export default JobPost;
