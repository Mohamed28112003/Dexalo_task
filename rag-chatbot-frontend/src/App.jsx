// src/App.jsx
import React, { useState } from 'react';
import Chat from './components/Chat';
import Sidebar from './components/Sidebar';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="container">
      <Sidebar isOpen={sidebarOpen} toggleSidebar={toggleSidebar} />
      <Chat toggleSidebar={toggleSidebar} />
    </div>
  );
}

export default App;
