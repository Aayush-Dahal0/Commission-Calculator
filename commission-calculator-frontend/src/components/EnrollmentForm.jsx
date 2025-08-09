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
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const [successMsg, setSuccessMsg] = useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const s = await api.get("/students");
        const c = await api.get("/courses");
        setStudents(s.data);
        setCourses(c.data);
      } catch (err) {
        setErrorMsg("Failed to load students or courses");
      }
    };
    fetchData();
  }, []);

  const enrollStudent = async (e) => {
    e.preventDefault();
    setErrorMsg("");
    setSuccessMsg("");
    setLoading(true);

    try {
      await api.post("/enrollments", {
        student_id: parseInt(studentId),
        course_id: parseInt(courseId),
        enrolled_at: enrolledAt,
        is_refunded: isRefunded,
        refund_date: isRefunded ? refundDate || null : null,
      });
      setSuccessMsg("Enrollment successful");
      setStudentId("");
      setCourseId("");
      setEnrolledAt("");
      setIsRefunded(false);
      setRefundDate("");
    } catch (err) {
      if (err.response?.data?.detail) {
        setErrorMsg(err.response.data.detail);
      } else {
        setErrorMsg("Enrollment failed. Server error.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="box">
      <h2>Enroll Student</h2>
      {errorMsg && <div style={{ color: "red" }}>{errorMsg}</div>}
      {successMsg && <div style={{ color: "green" }}>{successMsg}</div>}
      <form onSubmit={enrollStudent}>
        <select value={studentId} onChange={(e) => setStudentId(e.target.value)} required>
          <option value="">Select Student</option>
          {students.map((s) => (
            <option key={s.id} value={s.id}>
              {s.name} ({s.email})
            </option>
          ))}
        </select>

        <select value={courseId} onChange={(e) => setCourseId(e.target.value)} required>
          <option value="">Select Course</option>
          {courses.map((c) => (
            <option key={c.id} value={c.id}>
              {c.name}
            </option>
          ))}
        </select>

        <input type="date" value={enrolledAt} onChange={(e) => setEnrolledAt(e.target.value)} required />

        <label>
          <input
            type="checkbox"
            checked={isRefunded}
            onChange={(e) => setIsRefunded(e.target.checked)}
          />{" "}
          Refunded
        </label>

        {isRefunded && (
          <input
            type="date"
            value={refundDate}
            onChange={(e) => setRefundDate(e.target.value)}
          />
        )}

        <button type="submit" disabled={loading}>
          {loading ? "Enrolling..." : "Enroll"}
        </button>
      </form>
    </div>
  );
}
