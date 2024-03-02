import Link from 'next/link';
import React from 'react';

const ErrorCard: React.FC = () => {
  return (
    <div className="h-screen flex flex-col items-center justify-center max-lg:justify-start max-lg:pt-6 bg-card-bg">
      <h1 className="text-5xl font-bold text-primary mb-4 max-lg:mb-2 max-lg:text-xl">Oops!</h1>
      <h2 className="text-2xl font-semibold text-gray-600 mb-4 max-lg:mb-2 max-lg:text-sm">Something went wrong.</h2>
      <p className="text-lg text-gray-500 mb-8 max-lg:mb-2 max-lg:text-xs">We&apos;re sorry, but there was an error processing your request. Please try again later.</p>
      <Link href={'/'}>
      <button className="bg-primary hover:bg-primary text-white font-semibold py-2 px-4 rounded-md shadow-md transition-all duration-200  max-lg:py-1">
        Back to Home
      </button>
      </Link>
    </div>
  );
};

export default ErrorCard;