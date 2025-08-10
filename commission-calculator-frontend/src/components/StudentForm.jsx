import { useState, useEffect } from "react";
import api from "../api";

export default function StudentForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [students, setStudents] = useState([]);

  const fetchStudents = async () => {
    const res = await api.get("/students");
    setStudents(res.data);
  };

  const addStudent = async (e) => {
    e.preventDefault();
    try {
      await api.post("/students", { name, email });
      setName("");
      setEmail("");
      fetchStudents();
    } catch (err) {
      alert(err.response?.data?.detail || "Something went wrong");
    }
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  return (
    <div className="box">
      <h2 style={{ fontSize: "20px", fontWeight: "bold", marginBottom: "12px", color: "#333" }}>Add Student</h2>
      <form onSubmit={addStudent}>
        <input
          type="text"
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button type="submit">Add</button>
      </form>

      <h3>Student List</h3>
      <ul>
        {students.map((s) => (
          <li key={s.id}>
            {s.name} - {s.email}
          </li>
        ))}
      </ul>
    </div>
  );
}
