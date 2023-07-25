import React, { useState, useEffect } from "react";
import styles from "./UnitConversionPage.module.css";

const UnitConversionPage = () => {
  const [conversionDirection, setConversionDirection] = useState("kg-lb");
  const [inputValue, setInputValue] = useState("");
  const [outputValue, setOutputValue] = useState("");

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

  const handleToggleChange = () => {
    if (conversionDirection === "kg-lb") {
      setConversionDirection("lb-kg");
    } else {
      setConversionDirection("kg-lb");
    }
  };

  return (
    <div className={styles.container}>
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
