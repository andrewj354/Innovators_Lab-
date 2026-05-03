import React from 'react';

export default function Input({
  type = 'text',
  placeholder,
  required,
  value,
  onChange,
  name,
  error,
  className,
}) {
  return (
    <div className="input-group">
      <input
        type={type}
        placeholder={placeholder}
        required={required}
        value={value}
        onChange={onChange}
        name={name}
        className={className}
      />
      {error && <span className="input-error">{error}</span>}
    </div>
  );
}
