import { useState } from "react";
import axios from "axios";

const ResumeUpload = () => {
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        const formData = new FormData();
        formData.append("file", file);

        const token = localStorage.getItem("token");
        await axios.post("/api/resumes/resumes/", formData, {
            headers: {
                "Content-Type": "multipart/form-data",
                Authorization: `Bearer ${token}`,
            },
        });
        alert("Resume uploaded!");
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-4 border rounded">
            <h1 className="text-2xl mb-4">Upload Resume</h1>
            <form onSubmit={handleSubmit} className="space-y-4">
                <input type="file" onChange={handleFileChange} className="w-full" />
                <button type="submit" className="w-full bg-blue-500 text-white p-2 rounded">
                    Upload
                </button>
            </form>
        </div>
    );
};

export default ResumeUpload;
