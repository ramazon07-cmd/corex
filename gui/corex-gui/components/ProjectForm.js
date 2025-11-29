import { useState } from 'react';

export default function ProjectForm({ onSubmit, isGenerating }) {
  const [formData, setFormData] = useState({
    projectName: '',
    auth: 'session',
    ui: 'tailwind',
    database: 'sqlite',
    docker: false,
    api: false,
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/create-project', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });
      
      const result = await response.json();
      onSubmit(result);
    } catch (error) {
      onSubmit({
        success: false,
        message: 'Failed to create project',
        error: error.message
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Django Project</h2>
        <p className="text-gray-600 mb-6">
          Configure your Django project with authentication, UI framework, and database options.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div>
          <label htmlFor="projectName" className="block text-sm font-medium text-gray-700">
            Project Name
          </label>
          <input
            type="text"
            name="projectName"
            id="projectName"
            value={formData.projectName}
            onChange={handleChange}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="myproject"
          />
        </div>

        <div>
          <label htmlFor="auth" className="block text-sm font-medium text-gray-700">
            Authentication
          </label>
          <select
            id="auth"
            name="auth"
            value={formData.auth}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="session">Session (Traditional)</option>
            <option value="jwt">JWT (API/SPA)</option>
            <option value="allauth">Allauth (Social Login)</option>
          </select>
        </div>

        <div>
          <label htmlFor="ui" className="block text-sm font-medium text-gray-700">
            UI Framework
          </label>
          <select
            id="ui"
            name="ui"
            value={formData.ui}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="tailwind">Tailwind CSS</option>
            <option value="bootstrap">Bootstrap</option>
            <option value="none">None (API-only)</option>
          </select>
        </div>

        <div>
          <label htmlFor="database" className="block text-sm font-medium text-gray-700">
            Database
          </label>
          <select
            id="database"
            name="database"
            value={formData.database}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="sqlite">SQLite (Development)</option>
            <option value="postgres">PostgreSQL (Production)</option>
            <option value="mysql">MySQL</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div className="flex items-center">
          <input
            id="docker"
            name="docker"
            type="checkbox"
            checked={formData.docker}
            onChange={handleChange}
            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label htmlFor="docker" className="ml-2 block text-sm text-gray-900">
            Include Docker Configuration
          </label>
        </div>

        <div className="flex items-center">
          <input
            id="api"
            name="api"
            type="checkbox"
            checked={formData.api}
            onChange={handleChange}
            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label htmlFor="api" className="ml-2 block text-sm text-gray-900">
            Include Django REST Framework
          </label>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isGenerating || !formData.projectName}
          className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
            isGenerating || !formData.projectName
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
          }`}
        >
          {isGenerating ? 'Creating...' : 'Create Project'}
        </button>
      </div>
    </form>
  );
}