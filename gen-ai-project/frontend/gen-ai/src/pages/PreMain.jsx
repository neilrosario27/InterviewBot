// MainPage.js
import React from "react";
import { Link } from "react-router-dom";
import logo from "../pages/logo.jpeg";
import './PreMain.css'; // Import CSS file for additional styling

const PreMain = () => {
  return (
    <div className="main-container"> {/* Apply CSS class */}
      <div className="logo-container">
        <Link to="/text">
        <div class=" col-lg-6 py-5 py-lg-0 order-2 order-lg-1" data-aos="fade-right">
        <p className="typer"><span class="typed" data-typed-items="your personal translator, आपका अपना अनुवादक,तुमचा स्वतःचा अनुवादक, તમારા પોતાના અનુવાદક, আপনার ব্যক্তিগত অনুবাদক, നിങ്ങളുടെ സ്വന്തം വിവർത്തകൻ "></span></p>
      </div>
          <div className="logo-wrapper">
            <img src={logo} alt="Your Image" className="logo" />
            <h1 className="text" style={{color:"white"}}>Get Started</h1>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default PreMain;
