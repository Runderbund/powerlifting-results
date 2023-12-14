import React from "react";
import styles from "./HomePage.module.css";
import logo from "../../assets/images/BearLogo.jpeg";
import "../../App.css";

/**
 * HomePage is responsible for displaying the home page.
 * @component
 */
const HomePage = () => {
  return (
    <div className="container">
      <h1>Welcome to Bear Steel Powerlifting</h1>
      <img src={logo} alt="Logo" className={styles.logo} />
    </div>
  );
};

export default HomePage;
