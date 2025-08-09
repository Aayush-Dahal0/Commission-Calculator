import StudentForm from "./components/StudentForm";
import CourseForm from "./components/CourseForm";
import EnrollmentForm from "./components/EnrollmentForm";
import CommissionReport from "./components/CommissionReport";

export default function App() {
  return (
    <div style={{ padding: "20px" }}>
      <h1>Commission Calculator</h1>
      <StudentForm />
      <CourseForm />
      <EnrollmentForm />
      <CommissionReport />
    </div>
  );
}
