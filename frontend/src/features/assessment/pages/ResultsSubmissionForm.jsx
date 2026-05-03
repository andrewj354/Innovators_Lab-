import React, { useState } from 'react';
import '../pages/styles/ResultsSubmissionForm.css';
import Input from '../components/Input';
import Button from '../components/Button';

export default function ResultsSubmissionForm({ initialData = {}, isLocked = false }) {
  const [formData, setFormData] = useState({
    githubUrl: initialData.githubUrl || '',
    videoUrl: initialData.videoUrl || '',
    liveDemo: initialData.liveDemo || '',
    description: initialData.description || ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Валідація: GitHub URL обов'язковий
    if (!formData.githubUrl) {
      alert('GitHub URL is required!');
      return;
    }

    if (isLocked) {
      alert('Submissions are locked.');
      return;
    }

    console.log('Відправка даних на бекенд:', formData);
    // Тут буде твій fetch/axios запит (POST або PUT)
  };

  return (
    <div className="submission-wrapper">
      <div className="submission-container">
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Logo" alt="Innovators Lab" />
        </div>

        <h2>Submit Your Project</h2>
        
        {isLocked && (
          <div className="status-badge locked">Submission is locked</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label>GitHub Repository URL *</label>
            <Input 
              name="githubUrl"
              type="url" 
              placeholder="https://github.com/..." 
              required={true}
              value={formData.githubUrl}
              onChange={handleChange}
              disabled={isLocked}
            />
          </div>

          <div className="input-group">
            <label>Video Presentation URL</label>
            <Input 
              name="videoUrl"
              type="url" 
              placeholder="YouTube or Loom link" 
              value={formData.videoUrl}
              onChange={handleChange}
              disabled={isLocked}
            />
          </div>

          <div className="input-group">
            <label>Live Demo URL</label>
            <Input 
              name="liveDemo"
              type="url" 
              placeholder="Vercel or Netlify link" 
              value={formData.liveDemo}
              onChange={handleChange}
              disabled={isLocked}
            />
          </div>

          <div className="input-group">
            <label>Project Description</label>
            <textarea 
              name="description"
              className="custom-textarea"
              placeholder="Briefly describe your solution..."
              value={formData.description}
              onChange={handleChange}
              disabled={isLocked}
            />
          </div>

          <Button 
            type="submit" 
            className={`btn-submit ${isLocked ? 'btn-disabled' : ''}`}
            disabled={isLocked}
          >
            {isLocked ? 'Submissions Closed' : 'Save Results'}
          </Button>
        </form>
      </div>
    </div>
  );
}