import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import styles from "./MeetListPage.module.css";
import '../../App.css';

/**
 * MeetListPage component fetches and displays a list of meets.
 * @component
 */
const MeetListPage = () => {
  const [meets, setMeets] = useState([]);

  // Fetches meets data when the component mounts.
  useEffect(() => {
    const fetchMeets = async () => {
      const response = await axios.get("http://localhost:8000/meets/");
      setMeets(response.data.meets);
    };
    fetchMeets();
  }, []);

  // Renders a list of meets, each meet links to its individual meet page.
  return (
    <div className="container">
      <h1>Meets</h1>
      <div className="contentBox">
        {meets.map((meet) => (
          <div key={meet.meet_id}>
            <Link className={styles.meetLink} to={`/meet/${meet.meet_id}`}>{meet.meet_name}</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default MeetListPage;
