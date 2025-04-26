import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Login from "./components/Login";
import Register from "./components/Register";
import ResumeUpload from "./components/ResumeUpload";
import ResumeList from "./components/ResumeList";
import ResumeFeedback from "./components/ResumeFeedback";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute";

const App = () => {
  return (
    <Router>
      <AuthProvider>
        <Navbar />
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route
            path="/resumes"
            element={
              <ProtectedRoute>
                <ResumeList />
              </ProtectedRoute>
            }
          />
          <Route
            path="/upload"
            element={
              <ProtectedRoute>
                <ResumeUpload />
              </ProtectedRoute>
            }
          />
          <Route
            path="/feedback/:id"
            element={
              <ProtectedRoute>
                <ResumeFeedback />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Login />} />
          <Route
          path="/jobs"
          element={
            <ProtectedRoute>
              <JobList />
            </ProtectedRoute>
          }
          />
          <Route
            path="/jobs/post"
            element={
              <ProtectedRoute>
                <JobPost />
              </ProtectedRoute>
            }
          />
          <Route
            path="/jobs/:id"
            element={
              <ProtectedRoute>
                <JobDetail />
              </ProtectedRoute>
            }
          />
        </Routes>
      </AuthProvider>
    </Router>
  );
};

export default App;
