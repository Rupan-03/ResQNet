import { useState, useEffect } from 'react';

const useWebSocket = (url) => {
  const [ws, setWs] = useState(null);
  const [notification, setNotification] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const newWs = new WebSocket(url);
    setWs(newWs);

    newWs.onopen = () => {
      console.log('WebSocket connected');
      setIsLoading(false);
    };

    newWs.onmessage = (event) => {
      if (event.data) {
        try {
          const data = JSON.parse(event.data);
          setNotification(data);
        } catch (error) {
          console.error('Error parsing JSON:', error);
          setErrorMessage('Failed to parse notification data.');
        }
      }
    };

    newWs.onerror = (error) => {
      console.error('WebSocket error:', error);
      setErrorMessage('WebSocket connection error.');
    };

    newWs.onclose = () => {
      console.log('WebSocket closed');
      setErrorMessage('WebSocket connection closed.');
      // Reconnect WebSocket when it's closed
      setWs(new WebSocket(url));
    };

    return () => {
      newWs.close();
    };
  }, [url]);

  

  return { ws, notification, errorMessage, isLoading, connectWebSocket };
};
const connectWebSocket = () => {
    ws && ws.onopen && ws.onopen();
};

export default useWebSocket;

