import { RootState } from "@/store";
import React, { useState } from "react";
import { useSelector } from "react-redux";
import Image from "next/image";
import { chat_logo } from "@/public";

interface MessageCardProps {
  query: string;
}

const MessageCard: React.FC = () => {
  const messageHistory = useSelector((state: RootState) => state.ChatHistory);
  const [inputValue, setInputValue] = useState('');

  // const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
  //   event.preventDefault();
  //   // Handle form submission here
  //   // console.log('Submitted value:', inputValue);
  //   // Clear the input field after submission if needed
  //   setInputValue('');
  // };
  console.log(messageHistory)

  return (
    <div>
      <div data-testid="message-card" className="shadow-md">
        {/* Display message history */}
        {messageHistory.messages.map((message, index) => (
          <div key={index} className={typeof message === 'string' ? (message === "An error occurred while generating response. Please try again") ? "bg-red-50 p-7 w-full" : "bg-white p-7 w-full" : "bg-white w-full p-7"}>
            
            {typeof message === 'string' ? (
              <div className="chat-message">
              <div className="flex items-end justify-end">
                <div className="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-1 items-end">
                  <div>
                    <span className={`px-4 py-2 rounded-lg inline-block rounded-br-none bg-blue-600 text-white"`}>{message}</span>
                  </div>
                </div>
                {/* You can include the image here */}
              </div>
            </div>
            ) : (
              <div className="chat-message">
                <div className={message.value.sender === 'user' ? "flex items-end" : "flex items-end justify-end"}>
                  <div className="flex flex-col space-y-2 text-xs max-w-xs mx-2 order-1 items-end">
                    <div>
                      <span className={`px-4 py-2 rounded-lg inline-block rounded-br-none bg-blue-600 text-white"}`}>{message.value.text}</span>
                    </div>
                  </div>
                  {/* You can include the image here */}
                </div>
              </div>
            )}
          </div>
          
        ))}
        {messageHistory.messages.length > 2 && messageHistory.messages.every(message => typeof message !== 'object' || !message.isSuccess) && (
    <div className="bg-red-50 p-7 w-full">
        <p className="max-w-[600px] md:ml-[25%] text-red-600">There was an error processing your request.</p>
    </div>
)}
      </div>
    </div>
  );
};

export default MessageCard;


