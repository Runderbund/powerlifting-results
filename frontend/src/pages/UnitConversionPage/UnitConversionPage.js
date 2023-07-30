import React, { useState, useEffect } from "react";
import styles from "./UnitConversionPage.module.css";
import '../../App.css';

/**
 * UnitConversionPage provides a utility for converting between kilograms and pounds.
 * @component
 */
const UnitConversionPage = () => {
  // Stores the direction of the conversion (kg to lb or lb to kg)
  const [conversionDirection, setConversionDirection] = useState("kg-lb");

  // Stores the input value (the number to convert)
  const [inputValue, setInputValue] = useState("");

  // Stores the output value (the result of the conversion)
  const [outputValue, setOutputValue] = useState("");

  // Effect that triggers every time the input value or the conversion direction changes
  useEffect(() => {
    // Only performs the conversion if there is an input value
    if (inputValue !== "") {
      const inputNumber = Number(inputValue);
      if (conversionDirection === "kg-lb") {
        // Converts from kg to lb
        setOutputValue((inputNumber * 2.20462).toFixed(2));
      } else {
        // Converts from lb to kg
        setOutputValue((inputNumber / 2.20462).toFixed(2));
      }
    } else {
      // If the input value is empty, also clears the output value
      setOutputValue("");
    }
  }, [inputValue, conversionDirection]);
  
  // Handler for changing the conversion direction
  const handleToggleChange = () => {
    if (conversionDirection === "kg-lb") {
      setConversionDirection("lb-kg");
    } else {
      setConversionDirection("kg-lb");
    }
  };

  return (
    <div className="container">
      <h1>Unit Conversion</h1>
      <div className={styles.conversionBox}>
        <div className={styles.switchContainer}>
          <label>kg to lb</label>
          <label className={styles.switch}>
            <input type="checkbox" onChange={handleToggleChange} />
            <span className={styles.slider}></span>
          </label>
          <label>lb to kg</label>
        </div>
        <div>
          <input
            type="number"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </div>
        <h3>  Converted Weight: {outputValue} {conversionDirection === "kg-lb" ? "lb" : "kg"}</h3>
      </div>
    </div>
  );
};

export default UnitConversionPage;
