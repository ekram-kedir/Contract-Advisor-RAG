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
    </div> 
        <Chat setLoading = {setLoading} />  
    </div>  
  );
};

export default Index;
