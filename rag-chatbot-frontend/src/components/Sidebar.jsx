// src/components/Sidebar.jsx
import React, { useState, useEffect } from 'react';
import DocumentUpload from './DocumentUpload';
import { useChatContext } from '../context/ChatContext';
import { getDocuments, deleteDocument, deleteAllDocuments } from '../services/api';

function Sidebar({ isOpen, toggleSidebar }) {
  const [documents, setDocuments] = useState([]);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const { resetChat } = useChatContext();

  useEffect(() => {
    fetchDocuments();
  }, []);

  const fetchDocuments = async () => {
    try {
      const data = await getDocuments();
      setDocuments(data.documents || []);
    } catch (error) {
      console.error('Failed to fetch documents:', error);
    }
  };

  const handleUploadComplete = () => {
    fetchDocuments();
  };

  const handleDeleteDocument = async (filename) => {
    try {
      await deleteDocument(filename);
      fetchDocuments();
    } catch (error) {
      console.error('Failed to delete document:', error);
    }
  };

  const handleDeleteAllDocuments = async () => {
    if (window.confirm('Are you sure you want to delete all documents?')) {
      try {
        await deleteAllDocuments();
        fetchDocuments();
        resetChat();
      } catch (error) {
        console.error('Failed to delete all documents:', error);
      }
    }
  };

  const handleNewChat = () => {
    resetChat();
  };

  return (
    <>
      <div className={`sidebar ${isOpen ? 'open' : ''}`}>
        <div className="sidebar-header">
          <button className="new-chat-button" onClick={handleNewChat}>
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
              <line x1="12" y1="5" x2="12" y2="19" />
              <line x1="5" y1="12" x2="19" y2="12" />
            </svg>
            New Chat
          </button>
        </div>
        
        <div className="document-list">
          <h3 style={{ marginBottom: '0.5rem' }}>Documents ({documents.length})</h3>
          {documents.length > 0 ? (
            <>
              {documents.map((doc, index) => (
                <div key={index} className="document-item">
                  <span title={doc}>{truncateString(doc, 20)}</span>
                  <div className="document-actions">
                    <button
                      className="document-action-button"
                      onClick={() => handleDeleteDocument(doc)}
                      title="Delete document"
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="14"
                        height="14"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M3 6h18" />
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6" />
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2" />
                        <line x1="10" y1="11" x2="10" y2="17" />
                        <line x1="14" y1="11" x2="14" y2="17" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
              <button
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#ef4444',
                  cursor: 'pointer',
                  fontSize: '0.75rem',
                  marginTop: '1rem',
                  textDecoration: 'underline'
                }}
                onClick={handleDeleteAllDocuments}
              >
                Delete All Documents
              </button>
            </>
          ) : (
            <p style={{ fontSize: '0.875rem', color: '#d1d5db' }}>
              No documents uploaded yet
            </p>
          )}
        </div>
        
        <div className="upload-area">
          <button 
            className="upload-button"
            onClick={() => setShowUploadModal(true)}
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
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="17 8 12 3 7 8" />
              <line x1="12" y1="3" x2="12" y2="15" />
            </svg>
            Upload Documents
          </button>
        </div>
      </div>
      
      {showUploadModal && (
        <DocumentUpload
          onUploadComplete={handleUploadComplete}
          onClose={() => setShowUploadModal(false)}
        />
      )}
    </>
  );
}

const truncateString = (str, num) => {
  if (str.length <= num) {
    return str;
  }
  return str.slice(0, num) + '...';
};

export default Sidebar;