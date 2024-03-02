import React, { useState, useEffect } from "react";
import { useSelector, useDispatch } from "react-redux";
import Image from "next/image";
import { GrAttachment } from "react-icons/gr";
import { IoSendSharp, IoAdd } from "react-icons/io5";
import { RootState } from "@/store";
import ChatHistory, { clearMessages, addMessage } from "@/store/features/chat/message-history";
import { usePostChatBotMutation } from "@/store/features/chat/chat-api";
import { useFetchMessagesQuery } from "@/store/features/chat/chat-api"; // Add this import for fetching messages
import MessageCard from "@/components/chat/MessageCard";
import services from "@/data/chat/services.json";
import Service from "@/components/chat/Service";
import ServiceType, { ChatResponse, MessageHistory } from "@/types/chat/chat-types";
import { chat_logo } from "@/public";
import { useUploadAttachmentMutation } from '@/store/features/chat/chat-api';


const Index = () => {
  const messageHistory = useSelector((state: RootState) => state.ChatHistory);
  const [input, setInput] = useState("");
  const [isNewChat, setIsNewChat] = useState(true);
  const [buttonActive, setButtonActive] = useState(false);
  const dispatch = useDispatch();
  const ipaddress = useSelector((state: RootState) => state.IpSlice.ipAddress);
  const [postChat, { isLoading }] = usePostChatBotMutation();
  const { data: messages, isLoading: messagesLoading, isError: messagesError, refetch } = useFetchMessagesQuery();
  console.log(messages)
  const [uploadAttachment] = useUploadAttachmentMutation();


  useEffect(() => {
    refetch();
  }, [refetch]);

  const submitClickHandler = (e: React.FormEvent) => {
    e.preventDefault();
    setButtonActive(true);

    dispatch(addMessage(input));

    postChat({
      message: input,
      Address: ipaddress,
      isNewChat: isNewChat,
    })
      .unwrap()
      .then((response: ChatResponse) => {
        dispatch(addMessage(response));
        setButtonActive(false);
      })
      .catch((error) => {
        console.error("Error:", error);
        setButtonActive(false);
      });

    setIsNewChat(false);
    setInput("");
  };

  const newTopic = () => {
    setIsNewChat(true);
    dispatch(clearMessages());
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      try {
        const formData = new FormData();
        formData.append('file', file);
        // Call the uploadAttachment mutation and pass the FormData object
        const response = await uploadAttachment(formData).unwrap();
        console.log('File uploaded successfully:', response.success);
      } catch (error) {
        console.error('Error uploading file:', error);
      }
    }
  };


  function isSameDay(date1: Date, date2: Date): boolean {
    return (
      date1.getFullYear() === date2.getFullYear() &&
      date1.getMonth() === date2.getMonth() &&
      date1.getDate() === date2.getDate()
    );
  }

  function categorizeMessages(messages: MessageHistory[]){
    const today = new Date();
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);
    const lastWeek = new Date(today);
    lastWeek.setDate(lastWeek.getDate() - 7);
  
    const todayMessages: string[] = [];
    const yesterdayMessages: string[] = [];
    const lastWeekMessages: string[] = [];
  
    messages.forEach((message) => {
      const messageDate = new Date(message.content[1]);
      if (isSameDay(messageDate, today)) {
        todayMessages.push(message.content[0]);
      } else if (isSameDay(messageDate, yesterday)) {
        yesterdayMessages.push(message.content[0]);
      } else if (messageDate >= lastWeek) {
        lastWeekMessages.push(message.content[0]);
      }
    });
  
    return { todayMessages, yesterdayMessages, lastWeekMessages };
}
  
  if (messages){
    const categorizedMessages = categorizeMessages(messages);

  console.log(categorizedMessages, "here")
   

  
  return (
    <div className="flex flex-row min-h-screen relative bg-white"> 
      <div className="hidden md:block w-1/4">
      <aside id="default-sidebar" className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0" aria-label="Sidebar">
  <div className="h-full px-3 py-4 overflow-y-auto bg-white">
    <button onClick={newTopic} className="flex flex-row justify-center items-center border hover:shadow-chat-button rounded-full text-xl w-[200px] h-[36px] md:px-6 hover:bg-primary bg-[#56b2fd] capitalize text-white gap-2">
      <IoAdd className="text-white ml-[-36px]" size="1.4rem" />
      New Chat
    </button>
    {messages && categorizedMessages.todayMessages.length > 0 && (
  <div className="mt-6 ml-4">
    <h2 className="text-lg font-semibold mb-2">Todays Messages</h2>
    {/* Render only the latest message from today */}
    <div>{categorizedMessages.todayMessages[categorizedMessages.todayMessages.length - 1]}</div>
  </div>
)}
{messages && categorizedMessages.yesterdayMessages.length > 0 && (
  <div className="mt-6 ml-4">
    <h2 className="text-lg font-semibold mb-2">Yesterdays Messages</h2>
    {/* Render only the latest message from yesterday */}
    <div>{categorizedMessages.yesterdayMessages[categorizedMessages.yesterdayMessages.length - 1]}</div>
  </div>
)}
{messages && categorizedMessages.lastWeekMessages.length > 0 && (
  <div className="mt-6 ml-4">
    <h2 className="text-lg font-semibold mb-2">Last 7 Days Messages</h2>
    {/* Render only the latest message from last 7 days */}
    <div>{categorizedMessages.lastWeekMessages[categorizedMessages.lastWeekMessages.length - 1]}</div>
  </div>
)}

  </div>
</aside>

      </div>
      <div className="flex flex-col w-3/4">
        {messageHistory.messages && messageHistory.messages.length == 0 ? (
          <>
          
            <div className="ml-24 md:ml-[-24px]">
              <div className="flex  flex-col items-center min-h-[30vh] gap-2 max-sm:flex-col  justify-center pt-8 mb-6">
                <Image
                  src={chat_logo}
                  alt="Hakimhub's logo"
                  width={200}
                  height={200}
                />
                <p className="mt-2 text-5xl font-bold text-center  font-inter">
                  Welcome to Lizzy<span className="text-main">AI</span>
                </p>
                <p className="text-secondary-text text-xl text-center font-bold font-inter">
                  Your Ai-powered Contract Assistant 
                </p>
              </div>
            </div>
            <div className="ml-24 md:ml-[-24px]">
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
          </>
        ) : (
          <MessageCard />
        )}
        <div className="bottom-0 fixed ml-12 md:ml-16">
          <form className="flex flex-stretch w-[80vw] md:w-[64vw] py-2">
            <div className="flex w-full items-center shadow-md rounded-md p-2 bg-[rgb(248,246,246)]">
            <label htmlFor="file-upload" className="cursor-pointer flex items-center">
                <GrAttachment className="text-white" size="1.4rem" />
                <span className="ml-1">Attach File</span>
                <input
                  id="file-upload"
                  type="file"
                  className="hidden"
                  onChange={handleFileChange}
                  accept=".pdf, .doc, .docx, .txt"
                />
              </label>              <input
                className="appearance-none bg-transparent border-none w-full mr-3 px-2 focus:outline-none"
                type="text"
                placeholder="Ask me anything..."
                aria-label="message"
                value={input}
                onChange={(e) => {
                  setInput(e.target.value);
                }}
              />
              <button
                disabled={buttonActive}
                className="text-chat hover:text-main my-[5px]"
                onClick={(e) => submitClickHandler(e)}
              >
               
          
       
                <IoSendSharp size={24} />
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>  
  );
};
}
export default Index;
