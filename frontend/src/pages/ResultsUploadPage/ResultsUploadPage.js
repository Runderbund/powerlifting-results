import React, { useState } from "react";
import axios from "axios";
import styles from "./ResultsUploadPage.module.css";
import { useNavigate } from "react-router-dom";
import { useDropzone } from "react-dropzone";
import "../../App.css";

/**
 * ResultsUploadPage renders a form that allows the user to upload a CSV file with meet results.
 * @component
 */
const ResultsUploadPage = () => {
  // State variables for storing the meet ID, accepted CSV file, and email address
  const [meetId, setMeetId] = useState(null);
  const [acceptedFiles, setAcceptedFiles] = useState([]); // Do I need an array? I'm just using one file.
  const [email, setEmail] = useState("");

  const navigate = useNavigate();

  // Dropzone configuration for handling file drop
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: ".csv",
    onDrop: (acceptedFiles) => {
      setAcceptedFiles(acceptedFiles);
    },
  });

  // Function to handle form submission
  const handleSubmit = (event, emailAfterUpload = false) => {
    event.preventDefault();

    // Form data for file upload
    const formData = new FormData();
    formData.append("meetName", event.target.meetName.value);
    formData.append("meetDate", event.target.meetDate.value);
    formData.append("resultsFile", acceptedFiles[0]);

    // Axios post request to upload the file
    axios
      .post("http://localhost:8000/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response) => {
        console.log("File uploaded successfully");
        setMeetId(response.data.meetId);
        navigate("/uploadsuccess", {
          state: {
            meetId: response.data.meetId,
            changeLog: response.data.changeLog,
          },
        });

        // If emailAfterUpload is true, send an email
        if (emailAfterUpload) {
          window.location.href = `mailto:${email}?subject=Upload Successful&body=Your file has been uploaded successfully.`;
        }
      })
      .catch((error) => {
        console.log("File upload failed");
        console.log(error);
      });
  };

  // Render the form for file upload
  return (
    <div className="container">
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
        <div
          // Dropzone container. Checks if a file is hovered over the container and styles accordingly
          {...getRootProps()}
          className={isDragActive ? styles.dropzoneActive : styles.dropzone}
        >
          <input {...getInputProps()} />
          {acceptedFiles.length > 0 ? (
            // If a file is selected, displays the file name
            <p>{acceptedFiles[0].path}</p>
          ) : isDragActive ? (
            <p>Drop the file here.</p>
          ) : (
            <p>Drag and drop a results file here, or click to select file.</p>
          )}
        </div>
        <label>
          Meet Director Email:
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </label>
        <div className={styles.buttonContainer}>
          <button type="submit">Upload</button>
          {/* Button to email and submit is unavailable if email is not filled in. */}
          <button
            type="submit"
            onClick={(e) => handleSubmit(e, true)}
            disabled={!email}
            title={!email ? "Fill in Meet Director Email to enable." : ""}
          >
            Upload and Email
          </button>
        </div>
      </form>
    </div>
  );
};

export default ResultsUploadPage;
