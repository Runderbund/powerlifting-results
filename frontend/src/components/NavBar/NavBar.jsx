import React from "react";
import { useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import AuthContext from "../../context/AuthContext";
import styles from "./NavBar.module.css";

/**
 * The Navbar component provides a navigation bar at the top of the page.
 * It uses context to check if a user is logged in and adjusts the menu accordingly.
 * @returns {JSX.Element} The rendered JSX for the Navbar component.
 */
const Navbar = () => {
  
  // Use context to get the logout function and user information.
  const { logoutUser, user } = useContext(AuthContext);
  const navigate = useNavigate();

  return (
    <div className={styles.navBar}>
      <ul>
        {/* Standard links that are always present at the top of the page*/}
        <li className={styles.brand}><Link to="/"><b>Home</b></Link></li>
        <li className={styles.brand}><Link to="/lifterlist"><b>Lifters</b></Link></li>
        <li className={styles.brand}><Link to="/meetlist"><b>Meet Results</b></Link></li>
        <li className={styles.brand}><Link to="/unitconversion"><b>Unit Converter</b></Link></li>

        {/* This link only appears if the user is logged in, i.e., an admin*/}
        {user && (
          <li className={styles.brand}><Link to="/upload"><b>Upload</b></Link></li>
        )}

        {/* If the user is logged in, display a logout button. Otherwise, display a login button. */}
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
