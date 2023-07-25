import React, { useState } from "react";
import axios from "axios";
import styles from "./ResultsUploadPage.module.css";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";

const ResultsUploadPage = () => {
  const [meetId, setMeetId] = useState(null);
  const [acceptedFiles, setAcceptedFiles] = useState([]);
  const navigate = useNavigate();

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: ".csv",
    onDrop: (acceptedFiles) => {
      setAcceptedFiles(acceptedFiles);
    },
  });

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("meetName", event.target.meetName.value);
    formData.append("meetDate", event.target.meetDate.value);
    formData.append("resultsFile", acceptedFiles[0]);

    axios
      .post("http://localhost:8000/meets/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully");
        setMeetId(response.data.meetId);
        navigate("/uploadsuccess", { state: { meetId: response.data.meetId, changeLog: response.data.changeLog } });
      })
      .catch((error) => {
        console.log("File upload failed");
        console.log(error);
      });
  };

  return (
    <div className={styles.container}>
      <h1>Upload Meet Results</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Meet Name:
          <input type="text" name="meetName" required />
        </label>
        <label>
          Meet Date:
          <input type="date" name="meetDate" required />
        </label>
        <div {...getRootProps()} className={isDragActive ? styles.dropzoneActive : styles.dropzone}>
          <input {...getInputProps()} />
          {acceptedFiles.length > 0 ? (
            <p>{acceptedFiles[0].path}</p>
          ) : isDragActive ? (
            <p>Drop the file here.</p>
          ) : (
            <p>Drag and drop a results file here, or click to select file.</p>
          )}
        </div>
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default ResultsUploadPage;
