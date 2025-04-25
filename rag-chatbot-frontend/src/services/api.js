// src/services/api.js
const API_BASE_URL = 'http://localhost:8000';

export const sendQuery = async (query) => {
  try {
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    
    if (!response.ok) {
      throw new Error('Failed to get response');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const uploadDocuments = async (formData) => {
  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Upload failed');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
};

export const getDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents`);
    
    if (!response.ok) {
      throw new Error('Failed to fetch documents');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const deleteDocument = async (filename) => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents/${filename}`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete document');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};

export const deleteAllDocuments = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/documents`, {
      method: 'DELETE',
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete all documents');
    }
    
    return await response.json();
  } catch (error) {
    console.error('API error:', error);
    throw error;
  }
};



export const calculateMath = async (expression) => {
    try {
      const response = await fetch(`${API_BASE_URL}/math`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ expression }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to process math expression');
      }
      
      return await response.json();
    } catch (error) {
      console.error('API error:', error);
      throw error;
    }
  };