import { useState } from "react";
import api from "../api";

export default function CommissionReport() {
  const [report, setReport] = useState([]);
  const [downloadUrl, setDownloadUrl] = useState("");
  const [showReport, setShowReport] = useState(false);

  const fetchReport = async () => {
    if (showReport) {
      // If already showing, just hide it
      setShowReport(false);
      return;
    }

    try {
      const res = await api.get("/commission");
      setReport(res.data);
      setShowReport(true);
    } catch (err) {
      console.error("Error fetching report:", err);
    }
  };

  const downloadReport = async () => {
    try {
      const res = await api.get("/commission-report/download");
      setDownloadUrl(res.data.download_url);
    } catch (err) {
      console.error("Error downloading report:", err);
    }
  };

  return (
    <div className="box">
      <h2>Commission Report</h2>
      <button onClick={fetchReport}>
        {showReport ? "Hide Report" : "View Report"}
      </button>
      <button onClick={downloadReport}>Download Excel</button>

      {downloadUrl && (
        <a href={downloadUrl} target="_blank" rel="noopener noreferrer">
          Click to Download
        </a>
      )}

      {showReport && (
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
      )}
    </div>
  );
}
