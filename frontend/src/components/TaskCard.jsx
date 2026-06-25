import { useState } from 'react';

const STATUS_COLORS = {
  todo: 'bg-gray-100 text-gray-700',
  in_progress: 'bg-blue-100 text-blue-700',
  done: 'bg-green-100 text-green-700',
};

const PRIORITY_COLORS = {
  low: 'text-green-600',
  medium: 'text-yellow-600',
  high: 'text-red-600',
};

export default function TaskCard({ task, onUpdate, onDelete }) {
  const [loading, setLoading] = useState(false);

  const handleStatusChange = async (e) => {
    setLoading(true);
    await onUpdate(task.id, { status: e.target.value });
    setLoading(false);
  };

  return (
    <div className="bg-white rounded-lg shadow p-4 border border-gray-200 hover:shadow-md transition-shadow">
      <div className="flex justify-between items-start mb-2">
        <h3 className="font-semibold text-gray-800 text-sm">{task.title}</h3>
        <span className={`text-xs font-medium ${PRIORITY_COLORS[task.priority]}`}>
          {task.priority}
        </span>
      </div>
      {task.description && (
        <p className="text-gray-500 text-xs mb-3 line-clamp-2">{task.description}</p>
      )}
      <div className="flex items-center justify-between">
        <select
          value={task.status}
          onChange={handleStatusChange}
          disabled={loading}
          className={`text-xs px-2 py-1 rounded-full font-medium border-0 cursor-pointer ${STATUS_COLORS[task.status]}`}
        >
          <option value="todo">Todo</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button
          onClick={() => onDelete(task.id)}
          className="text-gray-400 hover:text-red-500 text-xs transition-colors"
        >
          Delete
        </button>
      </div>
    </div>
  );
}
