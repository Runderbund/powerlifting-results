import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import styles from "./LifterListPage.module.css";
import '../../App.css';

/**
 * LifterListPage Component
 * This component is responsible for displaying a list of lifters.
 * @component
 */
const LifterListPage = () => {
  /**
   * State hook to store lifters.
   * @type {Array} lifters - Array of lifter objects.
   */
  const [lifters, setLifters] = useState([]);

  /**
   * Effect hook to fetch lifters data when the component mounts.
   */
  useEffect(() => {
    /**
     * Function to fetch lifters data from the API.
     * @async
     */
    const fetchLifters = async () => {
      const response = await axios.get("http://localhost:8000/meets/lifters/");
      setLifters(response.data.lifters);
    };
    fetchLifters();
  }, []);

  /**
   * Renders the component.
   * It maps through the lifters array and creates a Link component for each lifter.
   * Each Link navigates to the lifter's individual page when clicked.
   */
  return (
    <div className="container">
      <h1>Lifters</h1>
      <div className="contentBox">
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
