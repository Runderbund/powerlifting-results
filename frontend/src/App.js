// General Imports
import { Routes, Route } from "react-router-dom";
//import "./App.css"; useful start, but interfering with my own modular styling.

// Pages Imports
import HomePage from "./pages/HomePage/HomePage";
import RegisterPage from "./pages/RegisterPage/RegisterPage";
import LoginPage from "./pages/LoginPage/LoginPage";
import LifterListPage from "./pages/LifterListPage/LifterListPage";
import LifterPage from "./pages/LifterPage/LifterPage";
import MeetResultsPage from "./pages/MeetResultsPage/MeetResultsPage";
import MeetListPage from "./pages/MeetListPage/MeetListPage";
import ResultsUploadPage from "./pages/ResultsUploadPage/ResultsUploadPage";
import UnitConversionPage from "./pages/UnitConversionPage/UnitConversionPage";

// Component Imports
import Navbar from "./components/NavBar/NavBar";

// Util Imports
import PrivateRoute from "./utils/PrivateRoute";

function App() {
  return (
    <div>
      <Navbar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/lifterlist" element={<LifterListPage />} />
        <Route path="/lifter/:id" element={<LifterPage />} />
        <Route path="/meetlist" element={<MeetListPage />} />
        <Route path="/meet/:id" element={<MeetResultsPage />} />
        <Route path="/unitconversion" element={<UnitConversionPage />} />
        <Route
          path="/upload"
          element={
            <PrivateRoute>
              <ResultsUploadPage />
            </PrivateRoute>
          }
        />
      </Routes>
    </div>
  );
}

export default App;