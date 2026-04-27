import React, { useState, useEffect } from 'react';
import { 
  AutoAwesome, 
  History, 
  CloudUpload, 
  AutoGraph, 
  Settings, 
  Article, 
  Psychology,
  Link,
  HelpOutline,
  BubbleChart
} from '@mui/icons-material';

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
          <Psychology fontSize="large" style={{ color: 'var(--accent-color)' }} />
          GenBrain
        </div>
        
        <div className="nav-item active">
          <AutoAwesome fontSize="small" />
          <span>Studio</span>
        </div>
        <div className="nav-item">
          <Article fontSize="small" />
          <span>Library</span>
        </div>
        <div className="nav-item">
          <AutoGraph fontSize="small" />
          <span>Graph</span>
        </div>
        
        <div style={{ marginTop: '2rem' }}>
          <span className="label" style={{ paddingLeft: '1rem', fontSize: '0.6rem', opacity: 0.5 }}>Recent Memory</span>
          {history.slice(0, 5).map((note, i) => (
            <div key={i} className="nav-item" style={{ fontSize: '0.75rem', padding: '0.6rem 1rem' }}>
              <History fontSize="inherit" style={{ opacity: 0.5 }} />
              <span style={{ overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {note.summary}
              </span>
            </div>
          ))}
        </div>

        <div style={{ marginTop: 'auto' }}>
          <div className="nav-item">
            <Settings fontSize="small" />
            <span>Settings</span>
          </div>
        </div>
      </div>

      <div className="main-container">
        <header>
          <h1>Synthesize Knowledge</h1>
          <p className="subtitle">High-fidelity AI processing for your complex data.</p>
        </header>

        <div className="workspace">
          <div className="editor-section">
            <span className="label">
              <Article fontSize="inherit" /> Input Source
            </span>
            <textarea 
              placeholder="Enter your research, notes, or long-form data..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
            />
            
            <div className="btn-group">
              <button 
                className="process-btn" 
                onClick={handleProcess}
                disabled={loading}
                style={{ flex: 1 }}
              >
                {loading ? 'Synthesizing...' : <><AutoAwesome fontSize="small" /> Process with AI</>}
              </button>
              
              <label className="process-btn secondary" style={{ cursor: 'pointer' }}>
                <CloudUpload fontSize="small" />
                <input type="file" hidden onChange={handleFileUpload} accept=".pdf,.txt,.md" />
              </label>
            </div>
          </div>

          <div className="result-section">
            <span className="label">
              <BubbleChart fontSize="inherit" /> Output Insight
            </span>
            {result ? (
              <div key={result.timestamp}>
                <div className="result-card">
                  <span className="label"><Article fontSize="inherit" /> Abstract</span>
                  <p className="summary-text">{result.summary}</p>
                </div>

                <div className="result-card">
                  <span className="label"><BubbleChart fontSize="inherit" /> Entities & Tags</span>
                  <div className="tags-container">
                    {result.tags.map((tag, i) => (
                      <span key={i} className="tag">#{tag}</span>
                    ))}
                  </div>
                </div>

                <div className="result-card">
                  <span className="label"><HelpOutline fontSize="inherit" /> Inquiries</span>
                  <div>
                    {result.questions.map((q, i) => (
                      <div key={i} className="question-item">{q}</div>
                    ))}
                  </div>
                </div>

                <div className="result-card">
                  <span className="label"><Link fontSize="inherit" /> Linked Memory</span>
                  {result.related_notes.length > 0 ? (
                    result.related_notes.map((note, i) => (
                      <div key={i} className="related-note">
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '5px' }}>
                          <span className="label" style={{ color: 'var(--accent-secondary)', fontSize: '0.6rem' }}>Semantic Match</span>
                          <span style={{ fontSize: '0.7rem', opacity: 0.5 }}>{(note.score * 100).toFixed(0)}%</span>
                        </div>
                        <p style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>{note.summary}</p>
                      </div>
                    ))
                  ) : (
                    <p style={{ color: 'var(--text-secondary)', fontSize: '0.8rem' }}>Generating connections...</p>
                  )}
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)', opacity: 0.3 }}>
                <Psychology style={{ fontSize: '5rem', marginBottom: '1rem' }} />
                <p>Waiting for synthesis...</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
}

export default App;
