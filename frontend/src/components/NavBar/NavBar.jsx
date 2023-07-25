import React from "react";
import { useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import styles from "./NavBar.module.css";

const Navbar = () => {
  
  const { logoutUser, user } = useContext(AuthContext);
  const navigate = useNavigate();
  return (
    <div className={styles.navBar}>
      <ul>
        <li className={styles.brand}>
          <Link to="/">
            <b>Home</b>
          </Link>
        </li>
        <li className={styles.brand}>
          <Link to="/lifterlist">
            <b>Lifters</b>
          </Link>
        </li>
        <li className={styles.brand}>
          <Link to="/meetlist">
            <b>Meet Results</b>
          </Link>
        </li>
        <li className={styles.brand}>
          <Link to="/unitconversion">
            <b>Unit Converter</b>
          </Link>
        </li>
        {user && (
          <li className={styles.brand}>
            <Link to="/upload">
              <b>Upload</b>
            </Link>
          </li>
        )}

        <li className={styles.brand}>
          {user ? (
            <button onClick={logoutUser}>Logout</button>
          ) : (
            <button onClick={() => navigate("/login")}>Login</button>
          )}
        </li>
      </ul>
    </div>
  );
};

export default Navbar;
