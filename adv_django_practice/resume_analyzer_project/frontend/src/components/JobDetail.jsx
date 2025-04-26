import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const JobDetail = () => {
    const { id } = useParams();
    const [job, setJob] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchJob = async () => {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.get(`/api/jobs/jobs/${id}/`, {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setJob(res.data);
            } catch (error) {
                console.error("Error fetching job:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchJob();
    }, [id]);

    if (loading) return <div className="text-center mt-10">Loading job details...</div>;
    if (!job) return <div className="text-center mt-10">Job not found</div>;

    return (
        <div className="max-w-3xl mx-auto mt-10 p-6 border rounded shadow">
            <h1 className="text-3xl font-bold mb-2">{job.title}</h1>
            <p className="text-xl text-gray-600 mb-4">{job.location} • ${job.salary}</p>
            
            <div className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Job Description</h2>
                <p className="whitespace-pre-line">{job.description}</p>
            </div>

            <div className="mb-6">
                <h2 className="text-xl font-semibold mb-2">Required Skills</h2>
                <div className="flex flex-wrap gap-2">
                    {job.required_skills.map((skill, index) => (
                        <span key={index} className="bg-blue-100 text-blue-800 px-3 py-1 rounded-full">
                            {skill}
                        </span>
                    ))}
                </div>
            </div>

            <div className="flex justify-between items-center border-t pt-4">
                <div>
                    <p className="text-sm text-gray-500">
                        Posted on: {new Date(job.created_at).toLocaleDateString()}
                    </p>
                    {job.updated_at !== job.created_at && (
                        <p className="text-sm text-gray-500">
                            Last updated: {new Date(job.updated_at).toLocaleDateString()}
                        </p>
                    )}
                </div>
                <button className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600">
                    Apply Now
                </button>
            </div>
        </div>
    );
};

export default JobDetail;