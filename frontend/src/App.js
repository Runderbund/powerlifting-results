// General Imports
import { Routes, Route } from "react-router-dom";
import "./App.css";

// Pages Imports
import HomePage from "./pages/HomePage/HomePage";
import RegisterPage from "./pages/RegisterPage/RegisterPage";
import LoginPage from "./pages/LoginPage/LoginPage";
import LifterListPage from "./pages/LifterListPage/LifterListPage";
import LifterPage from "./pages/LifterListPage/LifterPage";
import MeetResultsPage from "./pages/MeetResultsPage/MeetResultsPage";
import ResultsUploadPage from "./pages/ResultsUploadPage/ResultsUploadPage";
import UnitConversionPage from "./pages/UnitConversionPage/UnitConversionPage";


// Component Imports
import Navbar from "./components/NavBar/NavBar";

// Util Imports
// import PrivateRoute from "./utils/PrivateRoute";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/lifterlist" element={<LifterListPage />} />
        <Route path="/lifter" element={<LifterPage />} />
        <Route path="/meetresults" element={<MeetResultsPage />} />
        <Route path="/upload" element={<ResultsUploadPage />} />
        <Route path="/unitconversion" element={<UnitConversionPage />} />

      </Routes>
    </div>
  );
}

export default App;

/* <Route
  path="/"
  element={
    <PrivateRoute>
      <HomePage />
    </PrivateRoute>
  }
/> */