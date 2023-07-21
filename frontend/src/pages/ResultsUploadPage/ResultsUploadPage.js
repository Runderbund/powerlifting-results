import React from "react";
import styles from "./ResultsUploadPage.module.css";
import axios from "axios";

const ResultsUploadPage = () => {

  const handleSubmit = (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append("meetName", event.target.meetName.value);
    formData.append("meetDate", event.target.meetDate.value);
    formData.append("resultsFile", event.target.resultsFile.files[0]);

    axios
      .post("http://localhost:8000/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully");
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
        <label>
          Results File:
          <input type="file" name="resultsFile" required />
        </label>
        <button type="submit">Upload</button>
      </form>
    </div>
  );
};

export default ResultsUploadPage;

// TODO: Add drag and drop capability with react-dropzone
