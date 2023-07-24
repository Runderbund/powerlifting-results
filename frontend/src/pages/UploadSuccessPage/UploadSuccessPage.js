import { useLocation } from "react-router-dom";
import styles from "./UploadSuccessPage.module.css";

const UploadSuccessPage = () => {
  const location = useLocation();
  const meetId = location.state.meetId;

  const downloadResults = () => {
    window.location.href = `http://localhost:8000/meets/${meetId}/results/download/`;
  };

  return (
    <div className={styles.container}>
      <h1>File uploaded successfully</h1>
      <button onClick={downloadResults}>
        Download Results CSV
      </button>
    </div>
  );
};

export default UploadSuccessPage;
