import { useLocation } from "react-router-dom";
import styles from "./UploadSuccessPage.module.css";
import "../../App.css";

/**
 * UploadSuccessPage is responsible for displaying the upload status.
 * @component
 */
const UploadSuccessPage = () => {
  /**
   * Uses the useLocation hook to access the state passed from ResultsUploadPage.
   */
  const location = useLocation();
  const meetId = location.state.meetId;
  const changeLog = location.state.changeLog;

  /**
   * Function to trigger the download of the results.
   */
  const downloadResults = () => {
    window.location.href = `http://localhost:8000/${meetId}/results/download/`;
  };

  /**
   * Renders the component.
   * It maps through the changeLog array and creates a paragraph for each log message.
   */
  return (
    <div className="container">
      <h1>File Uploaded Successfully</h1>
      <div className={styles.messageBox}>
        {changeLog.map((log, index) => (
          <p key={index}>{log}</p>
        ))}
      </div>
      <button onClick={downloadResults}>Download Results CSV</button>
    </div>
  );
};

export default UploadSuccessPage;
