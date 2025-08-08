import StudentForm from "./components/StudentForm";

function App() {
  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        📊 Commission Calculator
      </h1>

      {/* Student Section */}
      <StudentForm />

      {/* Later we will add:
        <CourseForm />
        <EnrollmentForm />
        <CommissionReport />
      */}
    </div>
  );
}

export default App;
