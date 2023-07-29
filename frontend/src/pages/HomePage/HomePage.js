import React from "react";
import styles from "./HomePage.module.css";
import logo from "../../assets/images/BearLogo.jpg"
import '../../App.css';

/**
 * HomePage Component
 * This component is responsible for displaying the home page.
 * @component
 */
const HomePage = () => {
  /**
   * Renders the component.
   */
  return (
    <div className="container">
      <h1>Welcome to Bear Steel Powerlifting</h1>
      <img src={logo} alt="Logo" className={styles.logo}/>
    </div>
  );
};

export default HomePage;
