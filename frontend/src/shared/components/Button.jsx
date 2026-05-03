import React from 'react';

export default function Button({ children, type = 'button', className, onClick, disabled }) {
  return (
    <button
      type={type}
      className={className}
      onClick={onClick}
      disabled={disabled}
    >
      {children}
    </button>
  );
}
