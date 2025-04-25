// src/components/DocumentUpload.jsx
import React, { useState, useRef } from 'react';
import { uploadDocuments } from '../services/api';

function DocumentUpload({ onUploadComplete, onClose }) {
  const [files, setFiles] = useState([]);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles((prevFiles) => [...prevFiles, ...selectedFiles]);
    // Reset file input value to allow selecting the same file again
    e.target.value = null;
  };

  const handleDragEnter = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
    
    const droppedFiles = Array.from(e.dataTransfer.files);
    setFiles((prevFiles) => [...prevFiles, ...droppedFiles]);
  };

  const removeFile = (index) => {
    setFiles((prevFiles) => prevFiles.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    
    setIsUploading(true);
    setError(null);
    
    try {
      const formData = new FormData();
      files.forEach((file) => {
        formData.append('files', file);
      });
      
      await uploadDocuments(formData);
      onUploadComplete();
      onClose();
    } catch (err) {
      setError('Failed to upload documents. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="upload-modal">
      <div className="upload-modal-content">
        <div className="upload-modal-header">
          <h2 className="upload-modal-title">Upload Documents</h2>
          <button className="upload-modal-close" onClick={onClose}>&times;</button>
        </div>
        
        <div
          className={`upload-dropzone ${isDragging ? 'active' : ''}`}
          onDragEnter={handleDragEnter}
          onDragLeave={handleDragLeave}
          onDragOver={handleDragOver}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <p>Drag and drop files here, or click to select files</p>
          <p className="text-sm text-gray-500">Supported formats: PDF, TXT</p>
          <input
            type="file"
            ref={fileInputRef}
            onChange={handleFileChange}
            style={{ display: 'none' }}
            multiple
            accept=".pdf,.txt"
          />
        </div>
        
        {files.length > 0 && (
          <div className="upload-file-list">
            <h3>Selected Files ({files.length})</h3>
            {files.map((file, index) => (
              <div key={index} className="upload-file-item">
                <span className="upload-file-name">{file.name}</span>
                <button
                  className="upload-file-remove"
                  onClick={() => removeFile(index)}
                >
                  &times;
                </button>
              </div>
            ))}
          </div>
        )}
        
        {error && <p style={{ color: 'red', marginTop: '1rem' }}>{error}</p>}
        
        <div className="upload-footer">
          <button className="upload-cancel" onClick={onClose}>
            Cancel
          </button>
          <button
            className="upload-submit"
            onClick={handleUpload}
            disabled={files.length === 0 || isUploading}
          >
            {isUploading ? 'Uploading...' : 'Upload'}
          </button>
        </div>
      </div>
    </div>
  );
}

export default DocumentUpload;