'use client';
import { useState, useEffect, useRef } from 'react';

export default function Home() {
  const [logs, setLogs] = useState([]);
  const [testRunning, setTestRunning] = useState(false);
  const [apiUrl, setApiUrl] = useState('/api/test');
  const [concurrent, setConcurrent] = useState(10);
  const [delay, setDelay] = useState(1000);
  const runningRef = useRef(false);

  const fetchLogs = async () => {
    try {
      const res = await fetch('/api/logs');
      const data = await res.json();
      setLogs(data);
    } catch (e) {
      console.error('Failed to fetch logs:', e);
    }
  };

  useEffect(() => {
    fetchLogs();
    const interval = setInterval(fetchLogs, 1000);
    return () => clearInterval(interval);
  }, []);

  const startTest = async () => {
    setTestRunning(true);
    runningRef.current = true;
    const runBatch = async () => {
      if (!runningRef.current) return;
      const promises = [];
      for (let i = 0; i < concurrent; i++) {
        const payload = { microservice: `test-${Date.now()}-${i}`, timestamp: Date.now() };
        promises.push(fetch(apiUrl, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }));
        if (i % 2 === 0) {
          promises.push(fetch(apiUrl, { method: 'GET' }));
        }
      }
      await Promise.all(promises);
      setTimeout(runBatch, delay);
    };
    runBatch();
  };

  const stopTest = () => {
    setTestRunning(false);
    runningRef.current = false;
  };

  const totalPosts = logs.filter(l => l.method === 'POST').length;
  const totalGets = logs.filter(l => l.method === 'GET').length;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Microservices Load Test</h1>
      
      <div style={styles.controls}>
        <input style={styles.input} placeholder="API URL" value={apiUrl} onChange={e => setApiUrl(e.target.value)} />
        <input style={styles.input} type="number" placeholder="Concurrent" value={concurrent} onChange={e => setConcurrent(Number(e.target.value))} />
        <input style={styles.input} type="number" placeholder="Delay (ms)" value={delay} onChange={e => setDelay(Number(e.target.value))} />
        <button style={styles.startBtn} onClick={startTest}>Start Test</button>
        <button style={styles.stopBtn} onClick={stopTest}>Stop</button>
      </div>

      <div style={styles.stats}>
        <div style={styles.stat}><div style={styles.statValue}>{logs.length}</div><div style={styles.statLabel}>Total</div></div>
        <div style={styles.stat}><div style={styles.statValue}>{totalPosts}</div><div style={styles.statLabel}>POST</div></div>
        <div style={styles.stat}><div style={styles.statValue}>{totalGets}</div><div style={styles.statLabel}>GET</div></div>
      </div>

      <div style={styles.logsContainer}>
        <div style={styles.logsHeader}><h2>Request Logs</h2></div>
        <div style={styles.logs}>
          {logs.length === 0 ? <div style={styles.empty}>No requests yet</div> : 
            logs.slice().reverse().map((log, i) => (
              <div key={i} style={styles.log}>
                <span style={{...styles.logMethod, background: log.method === 'POST' ? '#e94560' : '#00d9ff'}}>{log.method}</span>
                <span style={styles.logPath}>{log.path}</span>
                <span style={styles.logBody}>{JSON.stringify(log.body || {}).substring(0, 80)}</span>
                <span style={styles.logTime}>{new Date(log.timestamp).toLocaleTimeString()}</span>
              </div>
            ))
          }
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: '1200px', margin: '0 auto', padding: '20px', background: '#1a1a2e', minHeight: '100vh', color: '#eee', fontFamily: 'system-ui, sans-serif' },
  title: { textAlign: 'center', color: '#00d9ff', marginBottom: '20px' },
  controls: { display: 'flex', gap: '15px', flexWrap: 'wrap', justifyContent: 'center', marginBottom: '20px' },
  input: { padding: '12px 15px', borderRadius: '5px', border: 'none', background: '#0f3460', color: '#fff', fontSize: '14px' },
  startBtn: { padding: '12px 25px', borderRadius: '5px', border: 'none', background: '#00d9ff', color: '#1a1a2e', fontWeight: 'bold', cursor: 'pointer' },
  stopBtn: { padding: '12px 25px', borderRadius: '5px', border: 'none', background: '#e94560', color: '#fff', fontWeight: 'bold', cursor: 'pointer' },
  stats: { display: 'flex', gap: '20px', justifyContent: 'center', marginBottom: '20px' },
  stat: { background: '#16213e', padding: '15px 25px', borderRadius: '10px', textAlign: 'center' },
  statValue: { fontSize: '24px', fontWeight: 'bold', color: '#00d9ff' },
  statLabel: { fontSize: '12px', color: '#888' },
  logsContainer: { background: '#16213e', borderRadius: '10px', overflow: 'hidden' },
  logsHeader: { background: '#0f3460', padding: '15px 20px' },
  logs: { maxHeight: '500px', overflowY: 'auto' },
  log: { padding: '12px 20px', borderBottom: '1px solid #0f3460', display: 'grid', gridTemplateColumns: '80px 1fr 150px 80px', gap: '15px', alignItems: 'center' },
  logMethod: { padding: '4px 8px', borderRadius: '4px', textAlign: 'center', fontWeight: 'bold', color: '#fff' },
  logPath: { color: '#fff' },
  logBody: { color: '#888', fontSize: '12px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' },
  logTime: { color: '#666', fontSize: '12px' },
  empty: { textAlign: 'center', padding: '40px', color: '#666' }
};
