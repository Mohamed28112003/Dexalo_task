// src/components/ChatInput.jsx
import React, { useState } from 'react';
import { useChatContext } from '../context/ChatContext';

const ChatInput = () => {
  const [query, setQuery] = useState('');
  const { sendMessage, isSending } = useChatContext();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isSending) {
      sendMessage(query);
      setQuery('');
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      handleSubmit(e);
    }
  };

  return (
    <div className="input-container">
      <form className="input-form" onSubmit={handleSubmit}>
        <textarea
          className="input-field"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask a question about your documents..."
          rows={1}
          disabled={isSending}
        />
        <button
          type="submit"
          className="send-button"
          disabled={!query.trim() || isSending}
        >
          {isSending ? (
            <div className="loading-spinner" />
          ) : (
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="16"
              height="16"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            >
              <line x1="22" y1="2" x2="11" y2="13" />
              <polygon points="22 2 15 22 11 13 2 9 22 2" />
            </svg>
          )}
        </button>
      </form>
    </div>
  );
};

export default ChatInput;