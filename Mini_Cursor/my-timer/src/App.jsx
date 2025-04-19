import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [time, setTime] = useState(0);
  const [running, setRunning] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    let timer;
    if (running) {
      timer = setInterval(() => {
        setTime(prevTime => prevTime + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [running]);

  const handleStartStop = () => {
    setRunning(!running);
  };

  const handleReset = () => {
    setRunning(false);
    setTime(0);
  };

  const toggleDarkMode = () => {
    setDarkMode(prevMode => !prevMode);
  };

  return (
    <div className={darkMode ? 'dark-mode' : 'light-mode'}>
      <h1>Timer: {time}s</h1>
      <button onClick={handleStartStop}>{running ? 'Stop' : 'Start'}</button>
      <button onClick={handleReset}>Reset</button>
      <button onClick={toggleDarkMode}>Toggle Dark/Light Mode</button>
    </div>
  );
}

export default App;
