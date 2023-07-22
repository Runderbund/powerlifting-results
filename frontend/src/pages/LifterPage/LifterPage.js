import React, { useState, useEffect } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import styles from "./LifterPage.module.css";

const LifterPage = () => {
  const { lifterId } = useParams();
  const [lifter, setLifter] = useState(null);
  const [results, setResults] = useState([]);

  useEffect(() => {
    const fetchLifterAndResults = async () => {
      const response = await axios.get(`http://localhost:8000/meets/lifters/${lifterId}`);
      setLifter(response.data.lifter[0]);
      setResults(response.data.results);
    };
    fetchLifterAndResults();
  }, [lifterId]);

  if (!lifter) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.lifterContainer}>
      <h1>{lifter.name}</h1>
      {results.map((result) => (
        <div key={result.result_id} className={styles.result}>
          <div>Meet ID: {result.meet}</div>
          <div>Division: {result.division}</div>
          <div>Total: {result.total}</div>
        </div>
      ))}
    </div>
  );
};

export default LifterPage;
