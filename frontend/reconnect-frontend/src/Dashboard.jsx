import { useState, useEffect } from 'react';
import { useNavigate, Routes, Route, Link } from 'react-router-dom';

function Home() {
  const [groupCount, setGroupCount] = useState(0);
  const [eventCount, setEventCount] = useState(0);
  const [messageCount, setMessageCount] = useState(0);

  useEffect(() => {
    // Fetch counts from API endpoints
    Promise.all([
      fetch('http://127.0.0.1:8000/api/groups/'),
      fetch('http://127.0.0.1:8000/api/events/'),
      fetch('http://127.0.0.1:8000/api/messages/')
    ])
    .then(([groupsRes, eventsRes, messagesRes]) => 
      Promise.all([groupsRes.json(), eventsRes.json(), messagesRes.json()])
    )
    .then(([groups, events, messages]) => {
      setGroupCount(groups.length);
      setEventCount(events.length);
      setMessageCount(messages.length);
    })
    .catch(err => console.error('Error fetching data:', err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-100">Welcome to Your Dashboard</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 hover:bg-gray-700 transition duration-300">
          <h3 className="text-lg font-semibold text-gray-200">Your Groups</h3>
          <p className="text-gray-400">{groupCount} Active Groups</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 hover:bg-gray-700 transition duration-300">
          <h3 className="text-lg font-semibold text-gray-200">Upcoming Events</h3>
          <p className="text-gray-400">{eventCount} Events</p>
        </div>
        <div className="bg-gray-800 p-6 rounded-lg shadow-lg border border-gray-700 hover:bg-gray-700 transition duration-300">
          <h3 className="text-lg font-semibold text-gray-200">Messages</h3>
          <p className="text-gray-400">{messageCount} Messages</p>
        </div>
      </div>
    </div>
  );
}

function Events() {
  const [events, setEvents] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/events/', {
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => {
        console.log('Received events data:', data); // Debug log
        setEvents(data);
      })
      .catch(err => {
        console.error('Error fetching events:', err);
        setError(err.message);
      });
  }, []);

  const handleRegister = (redirectUrl) => {
    if (!redirectUrl) {
      console.error('No redirect URL provided');
      return;
    }
    // Simple redirect to the URL
    window.location.href = redirectUrl;
  };

  if (error) {
    return <div className="text-red-500 p-4">Error: {error}</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-100">Events</h2>
      <div className="space-y-4">
        {events.map(event => (
          <div key={event.id} className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700 flex justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-200">{event.event_name}</h3>
            <p className="my-2 text-gray-400">{event.event_description} by {event.posted_by__username}</p></div>
            <div className="flex gap-2 h-[80%] m-auto mr-0">
              <button 
                onClick={() => handleRegister(event.event_reg_link)}
                className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition duration-300"
              >
                Register Now
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function Groups() {
  const [groups, setGroups] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    setIsLoading(true);
    fetch('http://127.0.0.1:8000/api/groups/', {
      credentials: 'include'
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log('Received groups data:', data);  // Debug log
        setGroups(data);
        setIsLoading(false);
      })
      .catch(err => {
        console.error('Error fetching groups:', err);
        setError(err.message);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) return <div className="p-6 text-gray-200">Loading groups...</div>;
  if (error) return <div className="p-6 text-red-500">Error: {error}</div>;
  if (!groups || groups.length === 0) {
    return <div className="p-6 text-gray-200">No groups found.</div>;
  }

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-100">Your Groups</h2>
      <div className="space-y-4">
        {groups.map(group => (
          <div key={group.id} className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700">
            <h3 className="text-lg font-semibold text-gray-200">{group.name}</h3>
            <button className="mt-4 bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 transition duration-300">
              View Group
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function Messages() {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/messages/', {
      credentials: 'include'
    })
      .then(res => res.json())
      .then(data => setMessages(data))
      .catch(err => console.error('Error fetching messages:', err));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6 text-gray-100">Messages</h2>
      <div className="space-y-4">
        {messages.map(message => (
          <div key={message.id} className="bg-gray-800 p-4 rounded-lg shadow-lg border border-gray-700">
            <p className="font-semibold text-gray-200">{message.sender__username}</p>
            <p className="my-2 text-gray-400">{message.content}</p>
            <p className="text-sm text-gray-500">
              {new Date(message.timestamp).toLocaleString()}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}

function Dashboard() {
  const navigate = useNavigate();

  const handleLogout = () => {
    fetch('/api/logout/', {
      method: 'POST',
      credentials: 'include'
    })
    .then(() => {
      navigate('/login');
    })
    .catch(err => console.error('Error logging out:', err));
  };

  return (
    <div className="min-h-screen bg-gray-900">
      <nav className="bg-gray-800 shadow-lg border-b border-gray-700 px-4 py-4">
        <div className="flex justify-between items-center">
          <div className="space-x-4">
            <Link 
              to="/dashboard"
              className="px-4 py-2 text-gray-300 hover:text-indigo-400 transition duration-300"
            >
              Home
            </Link>
            <Link
              to="/dashboard/events"
              className="px-4 py-2 text-gray-300 hover:text-indigo-400 transition duration-300"
            >
              Events
            </Link>
            <Link
              to="/dashboard/groups"
              className="px-4 py-2 text-gray-300 hover:text-indigo-400 transition duration-300"
            >
              Groups
            </Link>
            <Link
              to="/dashboard/messages"
              className="px-4 py-2 text-gray-300 hover:text-indigo-400 transition duration-300"
            >
              Messages
            </Link>
          </div>
          <button 
            className="bg-red-600 text-white px-4 py-2 rounded hover:bg-red-700 transition duration-300"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      </nav>

      <main>
        <Routes>
          <Route index element={<Home />} />
          <Route path="events" element={<Events />} />
          <Route path="groups" element={<Groups />} />
          <Route path="messages" element={<Messages />} />
        </Routes>
      </main>
    </div>
  );
}

export default Dashboard;
