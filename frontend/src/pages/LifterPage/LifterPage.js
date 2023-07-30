import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import styles from "./LifterPage.module.css";
import "../../App.css";

/**
 * LifterPage is responsible for displaying detailed information about a specific lifter.
 * @component
 */
const LifterPage = () => {
  // The `id` parameter from the current URL is retrieved using `useParams()`.
  const { id } = useParams();

  // `lifterData` state is initialized as null. This will hold the data about the lifter once it's fetched from the backend.
  const [lifterData, setLifterData] = useState(null);

  // `useEffect` is used to fetch the data about the lifter when the component first mounts or when `id` changes.
  useEffect(() => {
    const fetchLifterData = async () => {
      const response = await axios.get(`http://localhost:8000/lifters/${id}/`);
      setLifterData(response.data);
    };
    fetchLifterData();
  }, [id]);

  // Helper function to determine the style of lift (green or red background) results based on whether the lift was successful or not. Unsuccessful lifts begin with "-" in the imported CSV.
  const getLiftStyle = (lift) => {
    return lift >= 0 ? styles.successfulLift : styles.failedLift;
  };

  // Renders a loading message while the data is being fetched.
  if (!lifterData) {
    return <div>Loading...</div>;
  }

  // Once the data has been fetched, renders the lifter's data in a table.
  return (
    <div className="container">
      <h1>{lifterData.lifter[0].name}</h1>
      <table className={styles.result}>
        <thead>
          <tr>
            <th>Competition</th>
            <th>Date</th>
            <th>Placing</th>
            <th>Division</th>
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
          {lifterData.results.map((result) => (
            <tr key={result.result_id}>
              <td>
                <Link
                  className={styles.meetLink}
                  to={`/meet/${result.meet__meet_id}`}
                >
                  {result.meet__meet_name}
                </Link>
              </td>
              <td>{result.meet__meet_date}</td>
              <td>{result.placing}</td>
              <td>{result.division}</td>
              <td>{result.bodyweight}</td>
              <td className={getLiftStyle(result.squat1)}>{result.squat1}</td>
              <td className={getLiftStyle(result.squat2)}>{result.squat2}</td>
              <td className={getLiftStyle(result.squat3)}>{result.squat3}</td>
              <td className={getLiftStyle(result.bench1)}>{result.bench1}</td>
              <td className={getLiftStyle(result.bench2)}>{result.bench2}</td>
              <td className={getLiftStyle(result.bench3)}>{result.bench3}</td>
              <td className={getLiftStyle(result.deadlift1)}>
                {result.deadlift1}
              </td>
              <td className={getLiftStyle(result.deadlift2)}>
                {result.deadlift2}
              </td>
              <td className={getLiftStyle(result.deadlift3)}>
                {result.deadlift3}
              </td>
              <td>{result.total}</td>
              <td>{result.points}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default LifterPage;
