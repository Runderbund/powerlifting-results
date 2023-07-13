import React from "react";
import styles from "./HomePage.module.css";
import logo from "../../assets/images/BearLogo.jpg"

// import { useEffect, useState } from "react";
// import useAuth from "../../hooks/useAuth";

// import axios from "axios";

const HomePage = () => {
  return (
    <div className={styles.container}>
      <h1>Home Page Placeholder</h1>
      <img src={logo} alt="Logo" className={styles.logo}/>
      <h3> Welcome to Bear Steel Powerlifting</h3>
    </div>
  );
};

export default HomePage;
