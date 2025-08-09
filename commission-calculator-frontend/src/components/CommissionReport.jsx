import { useState } from "react";
import api from "../api";

export default function CommissionReport() {
  const [report, setReport] = useState([]);
  const [downloadUrl, setDownloadUrl] = useState("");

  const fetchReport = async () => {
    const res = await api.get("/commission");
    setReport(res.data);
  };

  const downloadReport = async () => {
    const res = await api.get("/commission-report/download");
    setDownloadUrl(res.data.download_url);
  };

  return (
    <div className="box">
      <h2>Commission Report</h2>
      <button onClick={fetchReport}>View Report</button>
      <button onClick={downloadReport}>Download Excel</button>
      {downloadUrl && <a href={downloadUrl} target="_blank">Click to Download</a>}
      <table>
        <thead>
          <tr>
            <th>Student</th>
            <th>Course</th>
            <th>Rate</th>
            <th>Amount</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          {report.map((r, idx) => (
            <tr key={idx}>
              <td>{r.student_name}</td>
              <td>{r.course_name}</td>
              <td>{r.commission_rate}</td>
              <td>{r.commission_amount}</td>
              <td>{r.commission_type}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
