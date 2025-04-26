import { useEffect, useState } from "react";
import axios from "axios";

const ResumeList = () => {
    const [resumes, setResumes] = useState([]);

    useEffect(() => {
        const fetchResumes = async () => {
            const token = localStorage.getItem("token");
            const res = await axios.get("/api/resumes/resumes/", {
                headers: { Authorization: `Bearer ${token}` },
            });
            setResumes(res.data);
        };
        fetchResumes();
    }, []);

    return (
        <div className="max-w-4xl mx-auto mt-10">
            <h1 className="text-2xl mb-6">My Resumes</h1>
            <div className="grid gap-4">
                {resumes.map((resume) => (
                    <div key={resume.id} className="p-4 border rounded shadow">
                        <p><strong>Status:</strong> {resume.status}</p>
                        <p><strong>Uploaded:</strong> {new Date(resume.created_at).toLocaleString()}</p>
                        {resume.status === 'parsed' && (
                            <a
                                href={`/feedback/${resume.id}`}
                                className="text-blue-500 underline"
                            >
                                View Feedback
                            </a>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default ResumeList;
