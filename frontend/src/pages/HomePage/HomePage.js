import React from "react";
import styles from "./HomePage.module.css";
import logo from "../../assets/images/BearLogo.jpg"
import '../../App.css';

const HomePage = () => {
  return (
    <div className="container">
      <h1>Welcome to Bear Steel Powerlifting</h1>
      <img src={logo} alt="Logo" className={styles.logo}/>
    </div>
  );
};

export default HomePage;
