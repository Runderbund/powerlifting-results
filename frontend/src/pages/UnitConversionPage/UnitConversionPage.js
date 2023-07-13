import React, { useState, useEffect } from "react";
import styles from "./UnitConversionPage.module.css";

/**
 * Allows the user to convert weights between kilograms and pounds.
 */
const UnitConversionPage = () => {
  // State variables for the conversion direction, input value, and output value
  const [conversionDirection, setConversionDirection] = useState("kg-lb");
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");

  /**
   * A side effect that runs when the inputValue or conversionDirection state variables change.
   * It converts the input value according to the current conversion direction and updates the outputValue state variable with the result. If the inputValue is an empty string, it clears the outputValue.
   */
  useEffect(() => {
    if (inputValue !== "") {
      const inputNumber = Number(inputValue);
      if (conversionDirection === "kg-lb") {
        setOutputValue((inputNumber * 2.20462).toFixed(2));
      } else {
        setOutputValue((inputNumber / 2.20462).toFixed(2));
      }
    } else {
      setOutputValue("");
    }
  }, [inputValue, conversionDirection]);

  return (
    <div className={styles.container}>
      <div className={styles.conversionBox}>
        <h1>Unit Conversion</h1>
        <div>
          <label>
            <input
              type="radio"
              value="kg-lb"
              checked={conversionDirection === "kg-lb"}
              onChange={(e) => setConversionDirection(e.target.value)}
            />
            kg to lb
          </label>
          <label>
            <input
              type="radio"
              value="lb-kg"
              checked={conversionDirection === "lb-kg"}
              onChange={(e) => setConversionDirection(e.target.value)}
            />
            lb to kg
          </label>
        </div>
        <div>
          <input
            type="number"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
          />
        </div>
        <div>Converted Weight: {outputValue}</div>
      </div>
    </div>
  );
};

export default UnitConversionPage;
