import { useState } from 'react';
import Header from './components/Header/Header';
import LogCard from './components/LogCard/LogCard';


function App() {
  const [logEntries, setLogEntries] = useState([
    { index: 1, log: "User 'admin' logged in successfully." },
    { index: 2, log: "File 'data.txt' uploaded to server." },
    { index: 3, log: "Error: Database connection timeout (retrying...)." },
    { index: 4, log: "System backup completed at 03:00 AM." },
    { index: 5, log: "Warning: Disk usage exceeds 85% on /dev/sda1." },
    { index: 6, log: "New user 'johndoe' registered with email 'john@example.com'." },
    { index: 7, log: "Security alert: 3 failed login attempts for user 'admin'." },
    { index: 8, log: "Scheduled task 'cleanup_temp_files' executed successfully." },
    { index: 9, log: "API request to '/v1/users' took 1243ms (slow response)." },
    { index: 10, log: "System shutdown initiated by user 'admin'." },
  ]);

return(<>
<Header/>
<div className='flex flex-col gap-y-4 max-h-96 overflow-y-scroll items-center'>
        {logEntries.map((logItem) => (
          <LogCard
            key={logItem.index}
            logIndex={logItem.index}
            logMessage={logItem.log}
          />
        ))}
      </div>
</>);
}

export default App;