import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import MainPage from "./pages/MainPage";
import Home from "./pages/Home";
import TextPage from "./pages/TextPage";
import AudioPage from "./pages/AudioPage";
import Navbar from "./components/Navbar";
import VivaPage from "./pages/VivaPage";
import SummaryPage from "./pages/SummaryPage";
import AuthenticatedWrapper from "./AuthenticatedWrapper"; // adjust the import path as needed
import PreMain from "./pages/PreMain";
import Audiopage2 from "./pages/Audiopage2";
import Home2 from "./pages/Home2";
import McqPage from "./pages/McqPage";
import UrlPage from "./pages/UrlPage";
import './App.css';
const App = () => {
  return (
    <div className="w-screen min-h-screen bg-img">

    <BrowserRouter>
   
      <Routes>

          <Route path="/text" element={<AuthenticatedWrapper><TextPage /></AuthenticatedWrapper>} />
          <Route path="/audio" element={<AuthenticatedWrapper><AudioPage /></AuthenticatedWrapper>} />

          <Route path="/summary" element={<AuthenticatedWrapper><SummaryPage/></AuthenticatedWrapper> } />
 
          <Route path="/audio2" element={<AuthenticatedWrapper><Audiopage2 /></AuthenticatedWrapper> } />

      </Routes>
    </BrowserRouter>
    </div>
  );
};

export default App;