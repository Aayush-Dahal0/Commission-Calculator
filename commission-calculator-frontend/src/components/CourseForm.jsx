import { useState, useEffect } from "react";
import api from "../api";

export default function CourseForm() {
  const [name, setName] = useState("");
  const [courseType, setCourseType] = useState("recorded");
  const [basePrice, setBasePrice] = useState("");
  const [courses, setCourses] = useState([]);

  const fetchCourses = async () => {
    const res = await api.get("/courses");
    setCourses(res.data);
  };

  const addCourse = async (e) => {
    e.preventDefault();
    await api.post("/courses", {
      name,
      course_type: courseType,
      base_price: parseFloat(basePrice),
    });
    setName("");
    setBasePrice("");
    fetchCourses();
  };

  useEffect(() => {
    fetchCourses();
  }, []);

  return (
    <div className="box">
      <h2>Add Course</h2>
      <form onSubmit={addCourse}>
        <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Course Name" required />
        <select value={courseType} onChange={(e) => setCourseType(e.target.value)}>
          <option value="recorded">Recorded</option>
          <option value="live">Live</option>
        </select>
        <input value={basePrice} onChange={(e) => setBasePrice(e.target.value)} placeholder="Base Price" type="number" required />
        <button type="submit">Add</button>
      </form>
      <h3>Course List</h3>
      <ul>
        {courses.map((c) => (
          <li key={c.id}>{c.name} ({c.course_type}) - NPR {c.base_price}</li>
        ))}
      </ul>
    </div>
  );
}
