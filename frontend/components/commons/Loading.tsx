const LoadingPage: React.FC = () => {
  return (
    <div role="load" className="flex items-center justify-center h-screen">
      <div role='load' data-testid="loading-spinner" className="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary"></div>
    </div>
  );
};

export default LoadingPage;
