import { useEffect, useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const JobList = () => {
    const [jobs, setJobs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchJobs = async () => {
            try {
                const token = localStorage.getItem("token");
                const res = await axios.get("/api/jobs/jobs/", {
                    headers: { Authorization: `Bearer ${token}` },
                });
                setJobs(res.data);
            } catch (error) {
                console.error("Error fetching jobs:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchJobs();
    }, []);

    if (loading) return <div className="text-center mt-10">Loading jobs...</div>;

    return (
        <div className="max-w-4xl mx-auto mt-10">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl">Available Jobs</h1>
                <Link 
                    to="/jobs/post" 
                    className="bg-green-500 text-white px-4 py-2 rounded"
                >
                    Post New Job
                </Link>
            </div>
            <div className="grid gap-4">
                {jobs.map((job) => (
                    <div key={job.id} className="p-4 border rounded shadow hover:shadow-md transition-shadow">
                        <h2 className="text-xl font-semibold">{job.title}</h2>
                        <p className="text-gray-600">{job.location} • ${job.salary}</p>
                        <div className="mt-2">
                            <p className="font-medium">Required Skills:</p>
                            <div className="flex flex-wrap gap-2 mt-1">
                                {job.required_skills.map((skill, index) => (
                                    <span key={index} className="bg-blue-100 text-blue-800 px-2 py-1 rounded text-sm">
                                        {skill}
                                    </span>
                                ))}
                            </div>
                        </div>
                        <p className="mt-2 text-gray-700 line-clamp-2">{job.description}</p>
                        <div className="mt-3 flex justify-between items-center">
                            <span className="text-sm text-gray-500">
                                Posted: {new Date(job.created_at).toLocaleDateString()}
                            </span>
                            <Link 
                                to={`/jobs/${job.id}`} 
                                className="text-blue-500 hover:underline"
                            >
                                View Details
                            </Link>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default JobList;