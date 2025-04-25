// src/components/Chat.jsx
import React, { useEffect, useRef } from 'react';
import ChatInput from './ChatInput';
import ChatMessage from './ChatMessage';
import { useChatContext } from '../context/ChatContext';

function Chat({ toggleSidebar }) {
  const { messages, isSending } = useChatContext();
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="chat-container">
      <button className="mobile-menu-button" onClick={toggleSidebar}>
        ☰
      </button>
      
      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="empty-chat">
            <h2 style={{ textAlign: 'center', marginTop: '20%', color: '#666' }}>
              Upload documents and start chatting with your data!
            </h2>
          </div>
        ) : (
          messages.map((message, index) => (
            <ChatMessage key={index} message={message} />
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <ChatInput />
    </div>
  );
}

export default Chat;