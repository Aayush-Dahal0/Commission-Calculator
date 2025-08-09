import { useState, useEffect } from "react";
import api from "../api";

export default function EnrollmentForm() {
  const [students, setStudents] = useState([]);
  const [courses, setCourses] = useState([]);
  const [studentId, setStudentId] = useState("");
  const [courseId, setCourseId] = useState("");
  const [enrolledAt, setEnrolledAt] = useState("");
  const [isRefunded, setIsRefunded] = useState(false);
  const [refundDate, setRefundDate] = useState("");

  const fetchData = async () => {
    const s = await api.get("/students");
    const c = await api.get("/allcourses");
    setStudents(s.data);
    setCourses(c.data);
  };

  const enrollStudent = async (e) => {
    e.preventDefault();
    await api.post("/enrolled", {
      student_id: parseInt(studentId),
      course_id: parseInt(courseId),
      enrolled_at: enrolledAt,
      is_refunded: isRefunded,
      refund_date: refundDate || null,
    });
    alert("Enrollment successful");
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="box">
      <h2>Enroll Student</h2>
      <form onSubmit={enrollStudent}>
        <select value={studentId} onChange={(e) => setStudentId(e.target.value)} required>
          <option value="">Select Student</option>
          {students.map((s) => (
            <option key={s.id} value={s.id}>{s.name}</option>
          ))}
        </select>
        <select value={courseId} onChange={(e) => setCourseId(e.target.value)} required>
          <option value="">Select Course</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>
        <input type="date" value={enrolledAt} onChange={(e) => setEnrolledAt(e.target.value)} required />
        <label>
          <input type="checkbox" checked={isRefunded} onChange={(e) => setIsRefunded(e.target.checked)} /> Refunded
        </label>
        {isRefunded && (
          <input type="date" value={refundDate} onChange={(e) => setRefundDate(e.target.value)} />
        )}
        <button type="submit">Enroll</button>
      </form>
    </div>
  );
}
