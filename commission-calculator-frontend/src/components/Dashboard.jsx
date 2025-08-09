import { useState } from "react";
import StudentForm from "./StudentForm";
import CourseForm from "./CourseForm";
import EnrollmentForm from "./EnrollmentForm";
import CommissionReport from "./CommissionReport";
import "./Dashboard.css";

export default function Dashboard() {
  const tabs = ["Students", "Courses", "Enrollments", "Commission Reports"];
  const [activeTab, setActiveTab] = useState(tabs[0]);

  const renderTabContent = () => {
    switch (activeTab) {
      case "Students":
        return <StudentForm />;
      case "Courses":
        return <CourseForm />;
      case "Enrollments":
        return <EnrollmentForm />;
      case "Commission Reports":
        return <CommissionReport />;
      default:
        return null;
    }
  };

  return (
    <div className="dashboard">
      <h1>Commission Calculator Dashboard</h1>
      <div className="tab-buttons">
        {tabs.map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={activeTab === tab ? "active" : ""}
          >
            {tab}
          </button>
        ))}
      </div>
      <div className="tab-content">{renderTabContent()}</div>
    </div>
  );
}
