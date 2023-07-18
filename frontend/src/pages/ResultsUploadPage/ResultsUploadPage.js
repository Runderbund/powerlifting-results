import React from "react";
import styles from "./ResultsUploadPage.module.css";

const ResultsUploadPage = () => {
  // Event handler for the form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    // Here you can handle the form data, for example, send it to a server
    console.log(event.target.meetName.value);
    console.log(event.target.meetDate.value);
    console.log(event.target.resultsFile.files[0]);
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