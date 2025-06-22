import React, { useState } from 'react';
import { FiSend } from 'react-icons/fi';
import '../styles/inputbar.css';

export default function InputBar({ input, setInput, onSend, loading }) {
  const [isFocused, setIsFocused] = useState(false);
  
  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      onSend();
    }
  };

  return (
    <div className="input-container">
      <div className={`input-bar ${isFocused ? 'focused' : ''} ${loading ? 'loading' : ''}`}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="Type your message..."
          disabled={loading}
          aria-label="Type your message"
        />
        
        <button 
          className="send-button" 
          onClick={onSend} 
          disabled={loading || !input.trim()}
          aria-label="Send message"
        >
          {loading ? (
            <div className="spinner"></div>
          ) : (
            <FiSend className="send-icon" />
          )}
        </button>
      </div>
    </div>
  );
}