import React from 'react';

const ChatMessage = ({ message }) => {
  const { role, content } = message;
  
  return (
    <div className={`message ${role === 'user' ? 'user-message' : 'assistant-message'}`}>
      <div className={`message-avatar ${role === 'user' ? 'user-avatar' : 'assistant-avatar'}`}>
        {role === 'user' ? 'U' : 'A'}
      </div>
      <div className="message-content">
        <div dangerouslySetInnerHTML={{ __html: formatContent(content) }} />
        
        {/* Sources section removed */}
      </div>
    </div>
  );
};

// Simple markdown-like formatting for code blocks
const formatContent = (content) => {
  if (!content) return '';
  
  // Format code blocks
  let formattedContent = content.replace(
    /```([\s\S]*?)```/g,
    '<pre><code>$1</code></pre>'
  );
  
  // Format line breaks
  formattedContent = formattedContent.replace(/\n/g, '<br>');
  
  return formattedContent;
};

export default ChatMessage;