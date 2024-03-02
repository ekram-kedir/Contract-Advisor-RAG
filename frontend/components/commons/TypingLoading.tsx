import { useEffect, useState } from 'react';

const TypingLoading = () => {
   
    const [dots, setDots] = useState('');
  
    useEffect(() => {
      const timer = setInterval(() => {
        setDots((prevDots) => (prevDots === '...' ? '.' : prevDots + '.'));
      }, 200);
  
      
  
      return () => clearInterval(timer);
    }, []);
  
    return (
      <div className="md:ml-[25%]  pl-4">
        
          <div className=" text-6xl text-primary">
            
            <span className="animate-pulse">{dots}</span>
          </div>
        
      </div>
    );
};

export default TypingLoading;
