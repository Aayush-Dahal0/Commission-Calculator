import { useState } from "react";
import StudentForm from "./components/StudentForm";
import CourseForm from "./components/CourseForm";
import EnrollmentForm from "./components/EnrollmentForm";
import CommissionReport from "./components/CommissionReport";
import "./Dashboard.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("students");

  return (
    <div className="dashboard">
      <div className="header">Commission Calculator</div>
      
      <div className="tab-buttons">
        <button
          className={activeTab === "students" ? "active" : ""}
          onClick={() => setActiveTab("students")}
        >
          Students
        </button>
        <button
          className={activeTab === "courses" ? "active" : ""}
          onClick={() => setActiveTab("courses")}
        >
          Courses
        </button>
        <button
          className={activeTab === "enrollments" ? "active" : ""}
          onClick={() => setActiveTab("enrollments")}
        >
          Enrollments
        </button>
        <button
          className={activeTab === "reports" ? "active" : ""}
          onClick={() => setActiveTab("reports")}
        >
          Commission Reports
        </button>
      </div>

      <div className="tab-content">
        {activeTab === "students" && <StudentForm />}
        {activeTab === "courses" && <CourseForm />}
        {activeTab === "enrollments" && <EnrollmentForm />}
        {activeTab === "reports" && <CommissionReport />}
      </div>
    </div>
  );
}
