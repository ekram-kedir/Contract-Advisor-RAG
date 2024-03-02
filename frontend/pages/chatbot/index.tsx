// import { usePostChatBotMutation } from "@/store/features/chat/chat-api";
// import {
//   pushMessage,
//   removeAllMessage,
// } from "@/store/features/chat/message-history";
// import { RootState } from "@/store";
// import { ChatResponse } from "@/types/chat/chat-types";
// import React, { useState, useRef, useEffect } from "react";
// import MessageCard from "@/components/chat/MessageCard";
// import {
//   IoChatbubbleEllipsesOutline,
//   IoSendSharp,
//   IoAdd,
// } from "react-icons/io5";
// import { 
//   useSelector,
//   useDispatch,
//  } from "react-redux";

// type SetStateFunction<T> = React.Dispatch<React.SetStateAction<T>>;
// type ChatProp = {
//   setLoading: SetStateFunction<boolean>;
// };
// const Chatbot: React.FC<ChatProp> = ({ setLoading }) => {
//   const [input, setInput] = useState("");
//   const [newChat, setNewChat] = useState(true);
//   const [buttonActive, setButtonActive] = useState(false);
//   const dispatch = useDispatch();
//   const ipaddress = useSelector((state: RootState) => state.IpSlice.ipAddress);
//   const [postChat, { isLoading }] = usePostChatBotMutation();
//   const inputRef = useRef<HTMLInputElement>(null);
//   const messages = useSelector((state:RootState) => state.ChatHistory.messages)

//   useEffect(() => {
//     const submitData = async () => {
//       try {
//         await fetch("/api/get-ip");
        
//       } catch (error) {
//       }
//     };

//     submitData();
//   }, []);

//   useEffect(() => {
//     if (!isLoading) {
//       inputRef.current?.focus();
//     }
//   }, [isLoading]);
//   const submitClickHandler = (e: React.FormEvent) => {
//     setButtonActive(true);
//     setLoading(true);
//     e.preventDefault();
//     dispatch(pushMessage(input));

//     postChat({
//       message: input,
//       Address: ipaddress,
//       isNewChat: newChat,
//     })
//       .unwrap()
//       .then((response: ChatResponse) => {
//         setLoading(false);
//         dispatch(pushMessage(response));
//         setButtonActive(false);
//       })
//       .catch((error) => {
//         setLoading(false);
//         dispatch(
//           pushMessage("An error occured while generating response.Please try again")
//         );
//         setButtonActive(false);
//       });
//     setNewChat(false);
//     setInput("");
//   };
//   const newTopic = () => {
//     setNewChat(true);
//     dispatch(removeAllMessage());
//     setLoading(false);
//   };
//   const chatHistory = [
//     { message: 'hey how are you', timestamp: 'Today' },
//     { message: 'hey how are you', timestamp: 'Today' },
//     { message: 'hey how are you', timestamp: 'Today' },
//     { message: 'hey how are you', timestamp: 'Today' },
//     { message: 'hey how are you', timestamp: 'Today' },
//     { message: 'hey how are you', timestamp: 'Yesterday' },
//     { message: 'hey how are you', timestamp: 'Yesterday' },
//     { message: 'hey how are you', timestamp: 'Yesterday' },
//     { message: 'hey how are you', timestamp: 'Yesterday' },
//     { message: 'hey how are you', timestamp: 'Yesterday' },
//     { message: 'hey how are you', timestamp: 'Last 7 days' },
//     { message: 'hey how are you', timestamp: 'Last 7 days' },
//     { message: 'hey how are you', timestamp: 'Last 7 days' },
//     { message: 'hey how are you', timestamp: 'Last 7 days' },
//     { message: 'hey how are you', timestamp: 'Last 7 days' },
//   ];

//   return (
    
//     <div className="flex md:flex-row">
//       <div className="hidden md:block p-4 md:w-1/4">How are you
//       <aside id="default-sidebar" className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
//         <div className="h-full px-3 py-4 overflow-y-auto bg-white">
//         <button onClick={newTopic} className="flex flex-row justify-center items-center border hover:shadow-chat-button rounded-full text-xl w-[200px] h-[36px] md:px-6 hover:bg-primary bg-[#56b2fd] capitalize text-white gap-2">
//         <IoAdd className="text-white ml-[-36px]" size="1.4rem" />
//         New Chat
//         </button>
//         <div className="mt-6 ml-4">
//           {chatHistory.map((chat, index) => (
//             <div key={index}>
//               {index === 0 || chat.timestamp !== chatHistory[index - 1].timestamp ? (
//                 <div className="mt-4">
//                   <h2 className="">{chat.timestamp}</h2>
//                   <p className="">{chat.message}</p>
//                 </div>
//               ) : (
//                 <p>{chat.message}</p>
//               )}
//             </div>
//           ))}
//         </div>
//         </div>
//       </aside>
//       </div>
//       <div className="md:w-3/4] bottom-0 fixed ml-12 md:ml-96">
//           <form className="flex flex-stretch w-[80vw] md:w-[50vw] py-2">
//             <div className="flex w-full items-center shadow-md rounded-md p-2 bg-[rgb(248,246,246)]">
//               <IoChatbubbleEllipsesOutline
//                 className="text-secondary-text hidden md:flex my-[6px]  "
//                 size={24}
//               />
//               <input
//                 ref={inputRef}
//                 className="appearance-none bg-transparent border-none w-full mr-3 px-2 focus:outline-none"
//                 type="text"
//                 placeholder="Ask me anything..."
//                 aria-label="message"
//                 value={input}
//                 onChange={(e) => {
//                   setInput(e.target.value);
//                 }}
//               />
//               <button
//                 disabled={buttonActive}
//                 className="text-chat hover:text-main my-[5px]"
//                 onClick={(e) => submitClickHandler(e)}
//               >
//                 <IoSendSharp size={24} />
//               </button>
//             </div>
//           </form>
//       </div>
//     </div>

//   );
// };
// export default Chatbot;

import React, {useState} from "react";
import Image from "next/image";
import { chat_logo } from "@/public";
import services from "@/data/chat/services.json";
import Service from "@/components/chat/Service";
import ServiceType from "@/types/chat/chat-types";
import Chat from "@/components/chat/Chat";
import MessageCard from "@/components/chat/MessageCard";
import { useSelector } from "react-redux";
import { RootState } from "@/store";
import { FC } from 'react';
import TypingLoading from "@/components/commons/TypingLoading";

const Index: FC = () => {
  const messages = useSelector((state:RootState) => state.ChatHistory.messages)
  const [loading,setLoading] = useState<boolean>(false)
  return (
    <div className="min-h-screen relative bg-white"> 
      <div className="max-w-screen-2xl min-h-[100vh]">
      <div className="flex flex-col mb-16 "> 
        <div className="flex-grow">
        {messages.length === 0 ?

          <div className="flex flex-col gap-2 ">
            <div className="flex  flex-col items-center min-h-[30vh] gap-2 max-sm:flex-col  justify-center pt-8 mb-6">
              <Image
                src={chat_logo}
                alt="Hakimhub's logo"
                width={100}
                height={100}
              />
            <p className="text-5xl font-bold text-center  font-inter">
             Welcome to Hakim<span className="text-main">Hub</span><span className="text-5xl">AI</span>
            </p>
            <p className="text-secondary-text text-xl text-center font-bold font-inter">
               Your AI-powered copilot for your health
            </p>
            </div>
            <div className="flex flex-col lg:flex-row justify-center items-center gap-4 lg:justify-around p-8">
              {services.map((service: ServiceType) => (
                <Service
                  key={service.id}
                  title={service.title}
                  detail={service.detail}   
                />
              ))}
            </div>
          </div>
          :
          <MessageCard/>
          }
        </div>
        {loading && <TypingLoading/>}     
      </div>
      <Chat setLoading = {setLoading} /> 
    </div>  
    </div>  
  );
};

export default Index;


// <aside id="default-sidebar" className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
//         <div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
//         <button onClick={newTopic} className="flex flex-row justify-center items-center border hover:shadow-chat-button rounded-full text-xl w-[200px] h-[36px] md:px-6 hover:bg-primary bg-[#56b2fd] capitalize text-white gap-2">
//         <IoAdd className="text-white ml-[-36px]" size="1.4rem" />
//         New Chat
//         </button>
//         <div className="mt-6">
//           {chatHistory.map((chat, index) => (
//             <div key={index}>
//               {index === 0 || chat.timestamp !== chatHistory[index - 1].timestamp ? (
//                 <div>
//                   <h2 className="">{chat.timestamp}</h2>
//                   <p className="">{chat.message}</p>
//                 </div>
//               ) : (
//                 <p>{chat.message}</p>
//               )}
//             </div>
//           ))}
//         </div>
//         </div>
//       </aside>