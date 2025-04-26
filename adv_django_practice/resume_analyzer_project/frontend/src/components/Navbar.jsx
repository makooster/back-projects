import { Link } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const Navbar = () => {
    const { user, logout } = useAuth();

    return (
        <nav className="flex justify-between items-center p-4 bg-gray-800 text-white">
            <div>
                <Link to="/" className="font-bold text-xl">Resume Analyzer</Link>
            </div>
            <div className="flex gap-4">
                {user ? (
                    <>
                        <Link to="/resumes">My Resumes</Link>
                        {user.role === "recruiter" && <Link to="/jobs">Jobs</Link>}
                        <button onClick={logout} className="bg-red-500 px-3 py-1 rounded">Logout</button>
                    </>
                ) : (
                    <>
                        <Link to="/login">Login</Link>
                        <Link to="/register">Register</Link>
                    </>
                )}
            </div>
        </nav>
    );
};

export default Navbar;
