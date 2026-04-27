import React, { useState } from 'react';
import '../pages/styles/JuryPage.css';
import Input from '../components/Input';
import Button from '../components/Button';
import { submitScore } from '../api/juryApi';

export default function JuryPage({ assignmentId }) {
  const [score, setScore] = useState('');
  const [feedback, setFeedback] = useState('');

  const handleGrade = async (e) => {
    e.preventDefault();
    console.log('Збереження оцінки...');
    try {
      await submitScore(assignmentId, { score, feedback });
      alert('Оцінку успішно збережено!');
    } catch (error) {
      console.error('Помилка:', error);
    }
  };

  return (
    <div className="jury-wrapper">
      <div className="jury-container">
        
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Jury" alt="ChatoPotamus Jury" />
        </div>

        <h2>Grade Submission</h2>

        <form onSubmit={handleGrade}>
          <Input 
            type="number" 
            placeholder="Enter score (0-100)" 
            required={true} 
            value={score}
            onChange={(e) => setScore(e.target.value)}
          />
          <Input 
            type="text" 
            placeholder="Feedback for student" 
            required={true} 
            value={feedback}
            onChange={(e) => setFeedback(e.target.value)}
          />

          <Button type="submit" className="btn-grade">
            Submit Grade
          </Button>
        </form>

        <div className="links-text">
          Unsure about criteria? <a href="#rubric">View grading rubric</a>
        </div>

        <div className="links-text">
          <a href="#back" className="bold">← Back to list</a>
        </div>

        <Button className="btn-google">
          <img src="https://upload.wikimedia.org/wikipedia/commons/5/53/Google_%22G%22_Logo.svg" alt="Google" />
          Import from Classroom
        </Button>

      </div>
    </div>
  );
}