import { useState, useEffect, useCallback } from 'react';
import useWebSocket from 'react-use-websocket';
import './App.css';
import Header from './components/Header/Header';
import LogCard from './components/LogCard/LogCard';

function App() {
  const [logEntries, setLogEntries] = useState([
    { index: 1, log: "User 'admin' logged in successfully.", level: "INFO" },
    { index: 2, log: "File 'data.txt' uploaded to server.", level: "INFO" },
    { index: 3, log: "Error: Database connection timeout (retrying...).", level: "ERROR" },
    { index: 4, log: "System backup completed at 03:00 AM.", level: "INFO" },
    { index: 5, log: "Warning: Disk usage exceeds 85% on /dev/sda1.", level: "WARNING" },
    { index: 6, log: "New user 'johndoe' registered with email 'john@example.com'.", level: "INFO" },
    { index: 7, log: "Security alert: 3 failed login attempts for user 'admin'.", level: "WARNING" },
    { index: 8, log: "Scheduled task 'cleanup_temp_files' executed successfully.", level: "INFO" },
    { index: 9, log: "API request to '/v1/users' took 1243ms (slow response).", level: "WARNING" },
    { index: 10, log: "System shutdown initiated by user 'admin'.", level: "CRITICAL" },
  ]);

  const [socketUrl, setSocketUrl] = useState('ws://localhost:8000/ws-logs');
  const [isManualConnect, setIsManualConnect] = useState(false);

  const {
    lastMessage,
    readyState,
    getWebSocket,
  } = useWebSocket(socketUrl, {
    onOpen: () => {
      console.log('WebSocket connection established');
      setIsManualConnect(false);
    },
    onClose: () => console.log('WebSocket connection closed'),
    onError: (event) => console.error('WebSocket error:', event),
    shouldReconnect: (closeEvent) => !isManualConnect,
    reconnectInterval: 3000,
  });

  useEffect(() => {
    if (lastMessage !== null) {
      try {
        const newLog = JSON.parse(lastMessage.data);
        setLogEntries(prev => {

          const newIndex = prev.length > 0 ? Math.max(...prev.map(item => item.index)) + 1 : 1;

          return [{
            index: newIndex,
            log: newLog.message,
            level: newLog.level,
            timestamp: newLog.timestamp
          }, ...prev];
        });
      } catch (err) {
        console.error('Error parsing WebSocket message:', err);
      }
    }
  }, [lastMessage]);

  const connectionStatus = {
    0: 'Connecting',
    1: 'Connected',
    2: 'Closing',
    3: 'Disconnected'
  }[readyState];

  const isConnected = readyState === 1;

  const handleConnect = useCallback(() => {
    if (!isConnected) {
      const ws = getWebSocket();
      if (ws) ws.close();
      setIsManualConnect(false);
    }
  }, [isConnected, getWebSocket]);

  const handleDisconnect = useCallback(() => {
    if (isConnected) {
      const ws = getWebSocket();
      if (ws) {
        setIsManualConnect(true);
        ws.close();
      }
    }
  }, [isConnected, getWebSocket]);

  return (
    <>
      <Header />

      <div className="connection-panel p-4 mb-4 bg-gray-100 rounded-lg flex justify-between items-center">
        <div>
          <span className={`inline-block w-3 h-3 rounded-full mr-2 ${isConnected ? 'bg-green-500' : 'bg-red-500'
            }`}></span>
          <span>WebSocket: {connectionStatus}</span>
          {!isConnected && (
            <span className="ml-2 text-yellow-600">(Not receiving live updates)</span>
          )}
        </div>
        <div>
          {!isConnected ? (
            <button
              onClick={handleConnect}
              className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded"
            >
              Connect
            </button>
          ) : (
            <button
              onClick={handleDisconnect}
              className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded"
            >
              Disconnect
            </button>
          )}
        </div>
      </div>

      <div className='flex flex-col gap-y-4 max-h-96 overflow-y-scroll items-center'>
        {logEntries.map((logItem) => (
          <LogCard
            key={logItem.index}
            logIndex={logItem.index}
            logMessage={logItem.log}
            logLevel={logItem.level}
          />
        ))}
      </div>

    </>
  );
}

export default App;