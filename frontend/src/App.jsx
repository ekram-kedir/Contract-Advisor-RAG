import "./App.css";
import './themes/default/main.scss';
import Home from "./pages/Home";
import { Route, Routes } from "react-router-dom";
import './index.css'; // Import Tailwind CSS

function App() {
  return (
    <>
      <div>
        <Routes>
          <Route path="/" element={<Home />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
