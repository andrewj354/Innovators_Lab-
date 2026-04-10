import React from 'react';

export default function Input({ type, placeholder, required }) {
  return (
    <div className="input-group">
      <input 
        type={type} 
        placeholder={placeholder} 
        required={required} 
      />
    </div>
  );
}