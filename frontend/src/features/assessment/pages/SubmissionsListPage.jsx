import React, { useState, useEffect } from 'react';
import '../pages/styles/SubmissionsListPage.css';
import Button from '../components/Button';

export default function SubmissionsListPage({ taskId }) {
  const [submissions, setSubmissions] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Ендпоінт: GET /api/tasks/{id}/submissions/
    fetch(`/api/tasks/${taskId}/submissions/`)
      .then((res) => res.json())
      .then((data) => {
        setSubmissions(data);
        setIsLoading(false);
      })
      .catch((err) => {
        console.error("Помилка завантаження сабмітів:", err);
        setIsLoading(false);
      });
  }, [taskId]);

  return (
    <div className="admin-wrapper">
      <div className="admin-container">
        
        <div className="logo">
          <img src="https://via.placeholder.com/80x80.png?text=Logo" alt="Innovators Lab" />
        </div>

        <h2>Project Submissions</h2>
        <p className="subtitle">Jury & Admin View Only</p>

        {isLoading ? (
          <div className="loading-text">Loading results...</div>
        ) : (
          <div className="table-responsive">
            <table className="submissions-table">
              <thead>
                <tr>
                  <th>Team / Student</th>
                  <th>GitHub</th>
                  <th>Video</th>
                  <th>Live Demo</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                {submissions.length > 0 ? (
                  submissions.map((sub) => (
                    <tr key={sub.id}>
                      <td className="bold">{sub.team_name || 'Unnamed Team'}</td>
                      <td>
                        <a href={sub.github_url} target="_blank" rel="noreferrer" className="link-cyan">GitHub</a>
                      </td>
                      <td>
                        {sub.video_url ? (
                          <a href={sub.video_url} target="_blank" rel="noreferrer" className="link-cyan">Watch</a>
                        ) : '—'}
                      </td>
                      <td>
                        {sub.live_demo ? (
                          <a href={sub.live_demo} target="_blank" rel="noreferrer" className="link-cyan">Demo</a>
                        ) : '—'}
                      </td>
                      <td>
                        <Button className="btn-review">Review</Button>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="5">No submissions found yet.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}

        <div className="links-text">
          Logged in as <strong>Admin/Jury</strong>. <a href="#logout">Log out</a>
        </div>
      </div>
    </div>
  );
}