import React, { useState } from 'react';
import '../pages/styles/SubmissionPage.css'; 
import Input from '../components/Input';
import Button from '../components/Button';
import { submitWork } from '../api/submissionsApi';

export default function SubmissionPage({ taskId }) {
  const [workLink, setWorkLink] = useState('');
  const [comment, setComment] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Відправка роботи...');
    submitWork(taskId, { workLink, comment });
  };

  return (
    <div className="submission-wrapper">
      <div className="submission-container">
        
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Task" alt="Innovators Lab" />
        </div>

        <h2>Submit your work to ChatoPotamus</h2>

        <form onSubmit={handleSubmit}>
          <Input 
            type="url" 
            placeholder="Link to your project" 
            required={true} 
            value={workLink}
            onChange={(e) => setWorkLink(e.target.value)}
          />
          <Input 
            type="text" 
            placeholder="Add a comment" 
            required={false} 
            value={comment}
            onChange={(e) => setComment(e.target.value)}
          />

          <Button type="submit" className="btn-submit">
            Submit task
          </Button>
        </form>

        <div className="links-text">
          Made a mistake? <a href="#edit">You can edit it later!</a>
        </div>

        <div className="links-text">
          Need help with the task? <a href="#docs" className="bold">View Docs.</a>
        </div>

        <Button className="btn-google">
          <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google" />
          Attach from Google Drive
        </Button>

      </div>
    </div>
  );
}