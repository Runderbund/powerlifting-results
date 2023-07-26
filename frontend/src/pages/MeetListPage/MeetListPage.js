import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import styles from "./MeetListPage.module.css";
import '../../App.css';


const MeetListPage = () => {
  const [meets, setMeets] = useState([]);

  useEffect(() => {
    const fetchMeets = async () => {
      const response = await axios.get("http://localhost:8000/meets/meets/");
      setMeets(response.data.meets);
    };
    fetchMeets();
  }, []);

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
