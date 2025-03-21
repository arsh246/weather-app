import React from 'react';

const ErrorMessage = ({ message }) => {
  if (!message) return null;
  return (
    <div style={{ color: 'red', fontSize: '14px' }}>
      {message}
    </div>
  );
};

export default ErrorMessage;
