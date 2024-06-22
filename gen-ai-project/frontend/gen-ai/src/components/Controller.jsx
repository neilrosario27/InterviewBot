import React, { useState } from "react";
import Title from "./Title";
import RecordMessage from "./RecordMessage";
import axios from "axios";
import Dropdown from "./Dropdown";

const Controller = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [messages, setMessages] = useState([]);
  const [selectedLanguage, setSelectedLanguage] = useState("english");
  const [jobDescription, setJobDescription] = useState("");
  const [experience, setExperience] = useState("");

  const createBlobUrl = (data) => {
    const blob = new Blob([data], { type: "audio/mpeg" });
    const url = window.URL.createObjectURL(blob);
    return url;
  };

  const handleStop = async (blobUrl) => {
    console.log(blobUrl);
    setIsLoading(true);
    // Append recorded message to messages
    const myMessage = { sender: "me", blobUrl: blobUrl };
    const messagesArr = [...messages, myMessage];

    // Convert blob URL to blob object
    fetch(blobUrl)
      .then((res) => res.blob())
      .then(async (blob) => {
        // Sending audio file to backend AND selected language
        const formData = new FormData();
        formData.append("audio", blob, "myFile.wav");
        formData.append("language", selectedLanguage);
        formData.append("jd", jobDescription);
        formData.append("exp", experience);

        // Send form data to endpoint
        await axios
          .post("http://localhost:8000/getaudio/", formData, {
            responseType: "arraybuffer",
          })
          .then((res) => {
            // What we are getting from backend is array buffer, so making a blob of it
            const blob = res.data;
            const audio = new Audio();
            audio.src = createBlobUrl(blob);

            // Append to audio
            const johnMessage = { sender: "chatbook", blobUrl: audio.src };
            messagesArr.push(johnMessage);
            setMessages(messagesArr);

            // Play audio
            setIsLoading(false);
            // audio.play();
          })
          .catch((err) => {
            console.log(err);
            setIsLoading(false);
          });
      });
    setIsLoading(false);
  };

  return (
    <div className="h-screen overflow-y-hidden">
      <Title setMessages={setMessages} />
      <div className="flex flex-col justify-betwwen h-full overflow-y-scroll pb-96">
        {/* Conversation */}
        <div className="mt-5 px-5">
          {messages.map((audio, index) => {
            return (
              <div
                key={index}
                className={
                  "flex flex-col " +
                  (audio.sender === "chatbook" && "flex items-end")
                }
              >
                {/* Sender */}
                <div className="mt-4">
                  <p
                    className={
                      audio.sender === "chatbook"
                        ? "text-right mr-2 italic text-green-500"
                        : "ml-2 italic text-blue-500"
                    }
                  >
                    {audio.sender}
                  </p>
                  {/* Audio message here */}
                  <audio
                    src={audio.blobUrl}
                    className="appearance-none"
                    controls
                  />
                </div>
              </div>
            );
          })}

          {messages.length === 0 && !isLoading && (
            <div className="flex flex-col items-center">
              <div className="text-center font-dark text-white italic mt-10">
                Send chatbook a message...
              </div>
              <Dropdown setSelectedLanguageMain={setSelectedLanguage} />
              <div className="mt-4">
                <input
                  type="text"
                  placeholder="Job Description"
                  value={jobDescription}
                  onChange={(e) => setJobDescription(e.target.value)}
                  className="p-2 border rounded"
                />
              </div>
              <div className="mt-4">
                <input
                  type="text"
                  placeholder="Experience"
                  value={experience}
                  onChange={(e) => setExperience(e.target.value)}
                  className="p-2 border rounded"
                />
              </div>
            </div>
          )}
          {isLoading && (
            <div className="text-center text-white italic mt-10 animate-pulse">
              Please wait a moment...
            </div>
          )}
        </div>

        {/* Recorder */}
        <div className="fixed bottom-0 w-full py-6 border-t text-center bg-gradient-to-r from-gray-800 to-gray-950">
          <div className="flex justify-center items-center w-full">
            <RecordMessage handleStop={handleStop} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Controller;
