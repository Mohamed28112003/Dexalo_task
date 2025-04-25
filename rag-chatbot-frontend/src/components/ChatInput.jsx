import React, { useState } from 'react';
import { useChatContext } from '../context/ChatContext';

const ChatInput = () => {
  const [query, setQuery] = useState('');
  const { sendMessage, processMathExpression, isSending } = useChatContext();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isSending) {
      sendMessage(query);
      setQuery('');
    }
  };

  const handleMathCalculation = () => {
    if (query.trim() && !isSending) {
      processMathExpression(query);
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
          placeholder="Ask a question about your documents or enter a math expression..."
          rows={1}
          disabled={isSending}
        />
        
        {/* Math Agent Button */}
        <button
  type="button"
  className="math-button"
  onClick={handleMathCalculation}
  disabled={!query.trim() || isSending}
  title="Calculate with Math Agent"
>
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
    <rect x="2" y="2" width="20" height="20" rx="2" ry="2"></rect>
    <line x1="8" y1="7" x2="16" y2="7"></line>
    <line x1="8" y1="11" x2="16" y2="11"></line>
    <line x1="8" y1="15" x2="12" y2="15"></line>
    <line x1="16" y1="15" x2="16" y2="17"></line>
  </svg>
</button>
        
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