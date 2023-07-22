import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import styles from "./LifterListPage.module.css";

const LifterListPage = () => {
  const [lifters, setLifters] = useState([]);

  useEffect(() => {
    const fetchLifters = async () => {
      const response = await axios.get("http://localhost:8000/meets/lifters/");
      setLifters(response.data.lifters);
    };
    fetchLifters();
  }, []);

  return (
    <div className={styles.lifterContainer}>
      <div className={styles.lifterList}>
        <h2>Lifters</h2>
        {lifters.map((lifter) => (
          <div key={lifter.member_id}>
            <Link className={styles.lifterLink} to={`/lifter/${lifter.member_id}`}>{lifter.name}</Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default LifterListPage;
