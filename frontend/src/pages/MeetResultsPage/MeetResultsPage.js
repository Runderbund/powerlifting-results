import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link, useParams } from "react-router-dom";
import styles from "./MeetResultsPage.module.css";
import "../../App.css";

/**
 * MeetResultsPage is responsible for displaying the results of a specific meet.
 * @component
 */
const MeetResultsPage = () => {
  const { id } = useParams(); // React Router hook to get the 'id' from the URL
  const [meetData, setMeetData] = useState(null); // State to store the meet data

  // Helper function to determine the CSS class based on the lift value. Unsuccessful lifts begin with "-" in the imported CSV.
  const getLiftStyle = (liftValue) =>
    liftValue < 0 ? styles.failedLift : styles.successfulLift;

  // Helper function to format the date string into a more readable format
  const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return `${date.getDate()} ${date.toLocaleString("default", {
      month: "long",
    })} ${date.getFullYear()}`;
  };

  // Effect to fetch the meet data from the server
  useEffect(() => {
    const fetchMeetData = async () => {
      const response = await axios.get(`http://localhost:8000/${id}/results/`);
      setMeetData(response.data);
    };
    fetchMeetData();
  }, [id]);

  // Returns a loading message if the meet data has not been fetched yet
  if (!meetData) {
    return <div>Loading...</div>;
  }

  // Once the data has been fetched, renders the meet results in a table
  return (
    <div className="container">
      <h1>
        {meetData.meet.meet_name} - {formatDate(meetData.meet.meet_date)}
      </h1>
      <table className={styles.result}>
        <thead>
          <tr>
            <th>Lifter</th>
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
              <td>
                <Link
                  className={styles.lifterLink}
                  to={`/lifter/${result.lifter__member_id}`}
                >
                  {result.lifter__name}
                </Link>
              </td>
              <td>{result.division}</td>
              <td>{result.weight_class}</td>
              <td>{result.placing}</td>
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

export default MeetResultsPage;
