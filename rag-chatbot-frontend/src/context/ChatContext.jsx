import React, { createContext, useContext, useState } from 'react';
import { sendQuery, calculateMath } from '../services/api';

const ChatContext = createContext();

export const useChatContext = () => useContext(ChatContext);

export const ChatProvider = ({ children }) => {
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false);

  const sendMessage = async (query) => {
    if (!query.trim()) return;
    
    // Add user message
    const userMessage = { role: 'user', content: query };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    
    setIsSending(true);
    
    try {
      // Send query to API
      const response = await sendQuery(query);
      
      // Add assistant message with response
      const assistantMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources || []
      };
      
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error sending query:', error);
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.'
      };
      
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

  const processMathExpression = async (expression) => {
    if (!expression.trim()) return;
    
    // Add user message
    const userMessage = { role: 'user', content: expression };
    setMessages((prevMessages) => [...prevMessages, userMessage]);
    
    setIsSending(true);
    
    try {
      // Send math expression to API
      const response = await calculateMath(expression);
      
      // Add assistant message with math result
      const assistantMessage = {
        role: 'assistant',
        content: `${response.expression} = ${response.result}`
      };
      
      setMessages((prevMessages) => [...prevMessages, assistantMessage]);
    } catch (error) {
      console.error('Error processing math expression:', error);
      
      // Add error message
      const errorMessage = {
        role: 'assistant',
        content: 'Sorry, I couldn\'t process this mathematical expression. Please check the syntax and try again.'
      };
      
      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsSending(false);
    }
  };

  const resetChat = () => {
    setMessages([]);
  };

  return (
    <ChatContext.Provider value={{ 
      messages, 
      isSending, 
      sendMessage, 
      processMathExpression,
      resetChat 
    }}>
      {children}
    </ChatContext.Provider>
  );
};