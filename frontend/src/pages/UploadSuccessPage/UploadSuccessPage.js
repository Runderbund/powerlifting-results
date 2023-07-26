import { useLocation } from "react-router-dom";
import styles from "./UploadSuccessPage.module.css";
import '../../App.css';

const UploadSuccessPage = () => {
  const location = useLocation();
  const meetId = location.state.meetId;
  const changeLog = location.state.changeLog;

  const downloadResults = () => {
    window.location.href = `http://localhost:8000/meets/${meetId}/results/download/`;
  };

  return (
    <div className="container">
      <h1>File uploaded successfully</h1>
      <div className={styles.messageBox}>
        {/* Maps over changeLog and displays each log message */}
        {changeLog.map((log, index) => (
          <p key={index}>{log}</p>
        ))}
      </div>
      <button onClick={downloadResults}>
        Download Results CSV
      </button>
    </div>
  );
};

export default UploadSuccessPage;