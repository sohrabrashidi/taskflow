import { useState, useEffect } from 'react';
import TaskCard from '../components/TaskCard';
import api from '../api/tasks';

const STATUSES = ['all', 'todo', 'in_progress', 'done'];

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [filter, setFilter] = useState('all');
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchTasks = async () => {
    setLoading(true);
    const params = filter !== 'all' ? { status: filter } : {};
    const { data } = await api.get('/tasks', { params });
    setTasks(data);
    setLoading(false);
  };

  useEffect(() => { fetchTasks(); }, [filter]);

  const createTask = async (e) => {
    e.preventDefault();
    if (!title.trim()) return;
    await api.post('/tasks', { title, description });
    setTitle('');
    setDescription('');
    fetchTasks();
  };

  const updateTask = async (id, changes) => {
    await api.put(`/tasks/${id}`, changes);
    fetchTasks();
  };

  const deleteTask = async (id) => {
    await api.delete(`/tasks/${id}`);
    fetchTasks();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-2xl font-bold text-gray-900 mb-6">TaskFlow</h1>

        <form onSubmit={createTask} className="bg-white rounded-lg shadow p-4 mb-6 flex gap-3">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="New task title..."
            className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <input
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Description (optional)"
            className="flex-1 border border-gray-300 rounded px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">
            Add Task
          </button>
        </form>

        <div className="flex gap-2 mb-4">
          {STATUSES.map((s) => (
            <button
              key={s}
              onClick={() => setFilter(s)}
              className={`px-3 py-1 rounded-full text-sm font-medium capitalize ${
                filter === s ? 'bg-blue-600 text-white' : 'bg-white text-gray-600 border border-gray-300'
              }`}
            >
              {s.replace('_', ' ')}
            </button>
          ))}
        </div>

        {loading ? (
          <p className="text-gray-400 text-sm">Loading...</p>
        ) : tasks.length === 0 ? (
          <p className="text-gray-400 text-sm">No tasks found.</p>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
            {tasks.map((t) => (
              <TaskCard key={t.id} task={t} onUpdate={updateTask} onDelete={deleteTask} />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
