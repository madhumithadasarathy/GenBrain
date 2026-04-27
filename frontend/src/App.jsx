import React, { useState, useEffect } from 'react';

function App() {
  const [inputText, setInputText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/notes');
      const data = await response.json();
      setHistory(data.reverse());
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const handleProcess = async () => {
    if (!inputText.trim()) return;
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/process', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });
      const data = await response.json();
      setResult(data);
      fetchHistory();
    } catch (error) {
      console.error('Error processing note:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setResult(data);
      fetchHistory();
    } catch (error) {
      console.error('Error uploading file:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="sidebar">
        <div className="logo">
          <span>🧠</span> GenBrain
        </div>
        <div className="nav-item active">
          <span>✨</span> New Note
        </div>
        <div className="nav-item">
          <span>📚</span> Knowledge Base
        </div>
        
        <div style={{ marginTop: '1rem', padding: '0 1rem' }}>
          <span className="label" style={{ fontSize: '0.7rem' }}>Recent Notes</span>
          {history.slice(0, 5).map((note, i) => (
            <div key={i} className="nav-item" style={{ fontSize: '0.85rem', padding: '0.5rem' }}>
              {note.summary.substring(0, 25)}...
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item">
            <span>⚙️</span> Settings
          </div>
        </div>
      </div>

      <div className="main-container">
        <header>
          <h1>GenBrain Studio</h1>
          <p className="subtitle">Transform your raw thoughts into connected knowledge.</p>
        </header>

        <div className="workspace">
          <div className="editor-section">
            <span className="label">Raw Note</span>
            <textarea 
              placeholder="Paste your thoughts here..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
            
            <div style={{ display: 'flex', gap: '10px' }}>
              <button 
                className="process-btn" 
                onClick={handleProcess}
                disabled={loading}
                style={{ flex: 1 }}
              >
                {loading ? 'Thinking...' : 'Synthesize'}
              </button>
              
              <label className="process-btn" style={{ flex: 1, textAlign: 'center', background: 'rgba(255,255,255,0.05)', border: '1px solid var(--border-color)', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer' }}>
                {loading ? '...' : 'Upload Doc'}
                <input type="file" hidden onChange={handleFileUpload} accept=".pdf,.txt,.md" />
              </label>
            </div>
          </div>

          <div className="result-section">
            {result ? (
              <div className="animate-in">
                <div className="result-card">
                  <span className="label">📝 AI Summary</span>
                  <p>{result.summary}</p>
                </div>

                <div className="result-card">
                  <span className="label">🔖 Extracted Tags</span>
                  <div className="tags-container">
                    {result.tags.map((tag, i) => (
                      <span key={i} className="tag">{tag}</span>
                    ))}
                  </div>
                </div>

                <div className="result-card">
                  <span className="label">❓ Follow-Up Questions</span>
                  <ul className="question-list">
                    {result.questions.map((q, i) => (
                      <li key={i} className="question-item">{q}</li>
                    ))}
                  </ul>
                </div>

                <div className="result-card">
                  <span className="label">🔗 Related Knowledge</span>
                  {result.related_notes.length > 0 ? (
                    result.related_notes.map((note, i) => (
                      <div key={i} className="related-note">
                        <span className="score">{(note.score * 100).toFixed(0)}% Match</span>
                        <p>{note.summary}</p>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: 'var(--text-secondary)' }}>No related notes found yet.</p>
                  )}
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                Your AI-powered insights will appear here.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
