import React, { useState } from 'react';
import TextInput from '../components/TextInput'; // Ensure this path matches your file structure
import {Link}  from "react-router-dom";
import logo from "../pages/logo.jpeg"
import mic from "../pages/mic.png"
import audio2 from "../pages/Audiopage2"
import './text.css'
const TextPage = () => {
  const [chatHistory, setChatHistory] = useState([]);

  const addToChatHistory = (userText, serverResponse) => {
    setChatHistory(prevHistory => [...prevHistory, { userText, serverResponse }]);
  };

  return (
    <div className="flex h-screen w-screen">
      
      {/* Sidebar (optional) */}
      <div className="bg-img text-white w-64 p-4 space-y-4 flex flex-col justify-center">

        <div className="text-xl font-semibold"><Link to="audio2">
              <div className="main-container"> {/* Apply CSS class */}
      <div className="logo-container">
        <Link to="/audio2">
          <div className="logo-wrapper bg-white rounded-lg" style={{}}>
            <img src={mic} alt="Your Image" className="logo height" style={{height:"100px", width:"100px", alignSelf:"center"}}/>
          </div>
          <h1 className="text" style={{color:"white", textAlign:""}}>Use Voice</h1>

        </Link>
      </div>
    </div>
          </Link></div>
      </div>
      {/* Main content */}
      <div className="flex flex-col flex-1">
        <div className="overflow-hidden p-4 space-y-4 bg-gray-100 flex-1">
          {chatHistory.map((chat, index) => (
            <div key={index} className="text-left space-y-2">
              <div className="inline-block bg-blue-300 rounded px-4 py-2 text-black">
                User: {chat.userText}
              </div>
              <div className="inline-block bg-gray-300 rounded px-4 py-2 text-black">
                Server: {chat.serverResponse}
              </div>
            </div>
          ))}
        </div>
        <TextInput updateTextValue={addToChatHistory} />
      </div>
    </div>
  );
};

export default TextPage;
