import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import axios from "axios";

const ResumeFeedback = () => {
    const { id } = useParams();
    const [feedback, setFeedback] = useState(null);

    useEffect(() => {
        const fetchFeedback = async () => {
            const token = localStorage.getItem("token");
            const res = await axios.get(`/api/feedback/feedback/${id}/`, {
                headers: { Authorization: `Bearer ${token}` },
            });
            setFeedback(res.data);
        };
        fetchFeedback();
    }, [id]);

    if (!feedback) return <div className="text-center mt-10">Loading Feedback...</div>;

    return (
        <div className="max-w-3xl mx-auto mt-10 p-4 border rounded">
            <h1 className="text-2xl mb-4">Resume Feedback</h1>
            <div className="space-y-4">
                <div>
                    <h2 className="text-xl font-semibold">Skill Gaps</h2>
                    <ul className="list-disc ml-6">
                        {feedback.skill_gaps.map((gap, index) => (
                            <li key={index}>{gap}</li>
                        ))}
                    </ul>
                </div>
                <div>
                    <h2 className="text-xl font-semibold">Formatting Tips</h2>
                    <p>{feedback.formatting_tips}</p>
                </div>
                <div>
                    <h2 className="text-xl font-semibold">ATS Keywords</h2>
                    <ul className="list-disc ml-6">
                        {feedback.ats_keywords.map((word, index) => (
                            <li key={index}>{word}</li>
                        ))}
                    </ul>
                </div>
            </div>
        </div>
    );
};

export default ResumeFeedback;
