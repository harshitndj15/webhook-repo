import { useEffect, useState } from "react";

function App() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    const fetchEvents = async () => {
      const res = await fetch("http://localhost:5000/events");
      const data = await res.json();
      setEvents(data);
    };

    fetchEvents();
    const interval = setInterval(fetchEvents, 15000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl mb-4">GitHub Events</h1>
      <ul>
        {events.map((e, idx) => (
          <li key={idx} className="mb-2">
            {e.event === "push" && `${e.author} pushed to ${e.to_branch} on ${e.timestamp}`}
            {e.event === "pull_request" && `${e.author} submitted a pull request from ${e.from_branch} to ${e.to_branch} on ${e.timestamp}`}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
