// React and context imports
import React, { useContext, useEffect } from "react";
import AuthContext from "../../context/AuthContext";

// Custom hook for form handling
import useCustomForm from "../../hooks/useCustomForm";

// Router and styles imports
import { Link } from "react-router-dom";
import styles from "./LoginPage.module.css";
import '../../App.css';

const LoginPage = () => {
  // Gets the loginUser function and isServerError flag from  AuthContext
  const { loginUser, isServerError } = useContext(AuthContext);

  // Setting the default form values
  const defaultValues = { username: "", password: "" };

  // Provides the form data, the change handler, the submit handler, and a reset function
  const [formData, handleInputChange, handleSubmit, reset] = useCustomForm(
    defaultValues,
    loginUser
  );

  // Uses an effect that resets the form when there is a server error
  useEffect(() => {
    if (isServerError) {
      reset();
    }
  }, [isServerError, reset]);

  return (
    <div className="container">
      <form className="contentBox" onSubmit={handleSubmit}>
        <label>
          Username:{" "}
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleInputChange}
          />
        </label>
        <label>
          Password:{" "}
          <input
            type="text"
            name="password"
            value={formData.password}
            onChange={handleInputChange}
          />
        </label>
        {isServerError ? (
          <p className={styles.error}>Login failed, incorrect credentials!</p>
        ) : null}
        <Link to="/register">Click to register!</Link>
        <button>Login!</button>
      </form>
    </div>
  );
};

export default LoginPage;
