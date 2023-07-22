import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import styles from './MeetResultsPage.module.css';

const MeetResultsPage = () => {
  const { id } = useParams();
  const [meetData, setMeetData] = useState(null);

  useEffect(() => {
    const fetchMeetData = async () => {
      const response = await axios.get(`http://localhost:8000/meets/${id}/results/`);
      setMeetData(response.data);
    };
    fetchMeetData();
  }, [id]);

  if (!meetData) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <h1>{meetData.meet.meet_name} - {meetData.meet.meet_date}</h1>
      <table className={styles.result}>
        <thead>
          <tr>
            <th>Division</th>
            <th>Bodyweight</th>
            <th>Weight Class</th>
            <th>Squat 1</th>
            <th>Squat 2</th>
            <th>Squat 3</th>
            <th>Bench 1</th>
            <th>Bench 2</th>
            <th>Bench 3</th>
            <th>Deadlift 1</th>
            <th>Deadlift 2</th>
            <th>Deadlift 3</th>
            <th>Total</th>
            <th>Points</th>
          </tr>
        </thead>
        <tbody>
          {meetData.results.map((result) => (
            <tr key={result.result_id}>
              <td>{result.division}</td>
              <td>{result.bodyweight}</td>
              <td>{result.weight_class}</td>
              <td>{result.squat1}</td>
              <td>{result.squat2}</td>
              <td>{result.squat3}</td>
              <td>{result.bench1}</td>
              <td>{result.bench2}</td>
              <td>{result.bench3}</td>
              <td>{result.deadlift1}</td>
              <td>{result.deadlift2}</td>
              <td>{result.deadlift3}</td>
              <td>{result.total}</td>
              <td>{result.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default MeetResultsPage;
