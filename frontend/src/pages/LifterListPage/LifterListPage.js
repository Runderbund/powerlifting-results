import React, { useState, useEffect } from "react";
import axios from "axios";
import { Link } from "react-router-dom";

const LifterListPage = () => {
  const [lifters, setLifters] = useState([]);

  useEffect(() => {
    const fetchLifters = async () => {
      const response = await axios.get("http://localhost:8000/lifters/");
      setLifters(response.data.lifters);
    };
    fetchLifters();
  }, []);

  return (
    <div className="container">
      <h1>Lifter Listing</h1>
      {lifters.map((lifter) => (
        <div key={lifter.member_id}>
          <Link to={`/lifter/${lifter.member_id}`}>{lifter.name}</Link>
        </div>
      ))}
    </div>
  );
};

export default LifterListPage;
