import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import styles from "./MeetResultsPage.module.css";

const MeetResultsPage = () => {
  const { id } = useParams();
  const [meetData, setMeetData] = useState(null);

  const getLiftStyle = (liftValue) => liftValue < 0 ? styles.failedLift : styles.successfulLift;

  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return `${date.getDate()} ${date.toLocaleString("default", {
      month: "long",
    })} ${date.getFullYear()}`;
  };

  useEffect(() => {
    const fetchMeetData = async () => {
      const response = await axios.get(
        `http://localhost:8000/meets/${id}/results/`
      );
      setMeetData(response.data);
    };
    fetchMeetData();
  }, [id]);

  if (!meetData) {
    return <div>Loading...</div>;
  }

  return (
    <div className={styles.container}>
      <h1>
        {meetData.meet.meet_name} - {formatDate(meetData.meet.meet_date)}
      </h1>
      <table className={styles.result}>
        <thead>
          <tr>
            <th>Division</th>
            <th>Weight Class</th>
            <th>Placing</th>

            <th>Bodyweight</th>
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
              <td>{result.weight_class}</td>
              <td>{result.placing}</td>
              <td>{result.bodyweight}</td>
              <td className={getLiftStyle(result.squat1)}>{result.squat1}</td>
              <td className={getLiftStyle(result.squat2)}>{result.squat1}</td>
              <td className={getLiftStyle(result.squat3)}>{result.squat1}</td>
              <td className={getLiftStyle(result.bench1)}>{result.bench1}</td>
              <td className={getLiftStyle(result.bench2)}>{result.bench1}</td>
              <td className={getLiftStyle(result.bench3)}>{result.bench1}</td>
              <td className={getLiftStyle(result.deadlift1)}>{result.bench1}</td>
              <td className={getLiftStyle(result.deadlift2)}>{result.bench1}</td>
              <td className={getLiftStyle(result.deadlift3)}>{result.bench1}</td>
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
