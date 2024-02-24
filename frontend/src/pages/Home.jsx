import  { useEffect, useRef, useState } from 'react';
import '../App.css'
import '@chatscope/chat-ui-kit-styles/dist/default/styles.min.css';
import { MainContainer, ChatContainer, MessageList, Message, MessageInput, TypingIndicator } from '@chatscope/chat-ui-kit-react';
import axios from 'axios';

function Home() {

  const fileInputRef = useRef(null);
  const [text, setText] = useState('');
  const [prompt, setPrompt] = useState('');

 
  useEffect(() => {
    if(text){
      setPrompt(`
      Answer the following question based on the information in the provided text:
      ${text}
      `)
    }
    else{
      setPrompt("")
    }
  }, [text]);

  const handleButtonClick = () => {
    fileInputRef.current.click();
  };



  const handleFileChange = async (event) => {
    const selectedFile = event.target.files[0];

    const formData = new FormData();
    formData.append('file', selectedFile);


  try {

      const response = await axios.post('http://127.0.0.1:5000/extract-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
        setText(response.data.data);
      } catch (error) {
        console.error(error);
      }

  };

  const systemMessage = { //  Explain things like you're talking to a software professional with 5 years of experience.
    "role": "system", "content": prompt
  }
  
  const [messages, setMessages] = useState([
  
  ]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = async (message) => {
    const newMessage = {
      message,
      direction: 'outgoing',
      sender: "user"
    };

  const newMessages = [...messages, newMessage];
  setMessages(newMessages);
    setIsTyping(true);
    await processMessageToChatGPT(newMessages);

  };

  async function processMessageToChatGPT(chatMessages) { 

    let apiMessages = chatMessages.map((messageObject) => {
      let role = "";
      if (messageObject.sender === "ChatGPT") {
        role = "assistant";
      } else {
        role = "user";
      }
      return { role: role, content: messageObject.message}

    });


  
    const apiRequestBody = {
      "model": "gpt-4-1106-preview",
      "messages": [
        systemMessage, 
        ...apiMessages 
      ]
    }

    console.log("apiRequestBody: ", apiRequestBody.messages)

        try {
          const response = await axios.post('http://127.0.0.1:5000/api/v1/chat', { message:apiRequestBody.messages});
          setMessages([...chatMessages, {
                message: response.data.data,
                sender: "ChatGPT"
              }]);
              setIsTyping(false);
  
        } catch (error) {
          console.error('Error fetching data:', error);
        }

  }

  const styles = {
    userMessage: {
      color: "black",
      backgroundColor: "orange",
    },
    chatGPTMessage: {
      color: "black",
      backgroundColor: "lavender", 
    },
  };


function CustomMessage({ model, ...props }) {
  const senderStyle = model.sender === "user" ? styles.userMessage : styles.chatGPTMessage;

  return (
    <div style={senderStyle} {...props}>
      
      {model.message}
    </div>
  );
}
  return (
    <div className="App" style={{ height: '90vh', margin: 'auto' }}>
      <div style={{ position: 'relative', height: '100%', width: '700px', margin: 'auto' }}>

        <MainContainer style={{ padding: '10px 5px', borderRadius: '10px', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: 'auto' }}>
          <ChatContainer>
            <MessageList scrollBehavior="smooth" typingIndicator={isTyping ? <TypingIndicator content="Contract Advisor is typing"/> : null}>
              {messages.map((message, i) => {
                const messageAlignment = message.sender === "user" ? "right" : "left";

                return <div style={{ justifyContent: messageAlignment }}>
                        <CustomMessage key={i} model={message} />
                      </div>
              })}
            </MessageList>
            <MessageInput onSend={handleSend} style={{ textAlign: 'left' , color: '#FFFFFF' }} placeholder="Type message here" />
          </ChatContainer>
        </MainContainer>
      </div>
    </div>
  );
}

export default Home;


