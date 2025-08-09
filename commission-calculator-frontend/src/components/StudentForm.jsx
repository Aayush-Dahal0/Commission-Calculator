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
    <div className="p-4 border rounded">
      <h2 className="text-lg font-bold mb-2">Add Student</h2>
      <form onSubmit={addStudent} className="space-y-2">
        <input
          type="text"
          placeholder="Name"
          className="border p-2 w-full"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="border p-2 w-full"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <button className="bg-blue-500 text-white px-4 py-2 rounded">
          Add
        </button>
      </form>

      <h3 className="mt-4 font-bold">Student List</h3>
      <ul>
        {students.map((s) => (
          <li key={s.id}>{s.name} - {s.email}</li>
        ))}
      </ul>
    </div>
  );
}
