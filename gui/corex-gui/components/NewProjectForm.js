import { useState } from 'react';

export default function NewProjectForm({ onSubmit }) {
  const [formData, setFormData] = useState({
    projectName: '',
    template: 'ecommerce',
    auth: 'session',
    ui: 'tailwind',
    database: 'sqlite',
    docker: false,
    api: false,
  });

  const [isGenerating, setIsGenerating] = useState(false);
  const [progress, setProgress] = useState([]);
  const [websocket, setWebsocket] = useState(null);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const connectToAgent = () => {
    // In a real implementation, we would read the token from .corex_token file
    const token = 'sample-token'; // This would be loaded from the file
    const ws = new WebSocket('ws://localhost:8765');
    
    ws.onopen = () => {
      // Authenticate with the agent
      ws.send(JSON.stringify({
        type: 'auth',
        token: token
      }));
    };
    
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setProgress(prev => [...prev, data]);
      
      if (data.type === 'complete') {
        setIsGenerating(false);
        onSubmit({
          success: data.exit_code === 0,
          message: data.exit_code === 0 ? 'Project created successfully!' : 'Project creation failed',
          progress: [...progress, data]
        });
      } else if (data.type === 'error') {
        setIsGenerating(false);
        onSubmit({
          success: false,
          message: 'Project creation failed',
          error: data.message,
          progress: [...progress, data]
        });
      }
    };
    
    ws.onerror = (error) => {
      console.error('WebSocket error:', error);
      setIsGenerating(false);
      onSubmit({
        success: false,
        message: 'Failed to connect to CoreX Agent',
        error: error.message
      });
    };
    
    setWebsocket(ws);
    return ws;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsGenerating(true);
    setProgress([]);
    
    try {
      // Connect to CoreX Agent
      const ws = connectToAgent();
      
      // Wait for connection to establish
      setTimeout(() => {
        // Send command to create project
        ws.send(JSON.stringify({
          type: 'execute',
          command: `corex new ${formData.projectName} --template ${formData.template} --auth ${formData.auth} --ui ${formData.ui} --database ${formData.database} ${formData.docker ? '--docker' : ''} ${formData.api ? '--api' : ''}`,
          cwd: process.env.HOME
        }));
      }, 1000);
      
    } catch (error) {
      setIsGenerating(false);
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
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Industry Project</h2>
        <p className="text-gray-600 mb-6">
          Configure your industry-specific Django project with authentication, UI framework, and database options.
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
          <label htmlFor="template" className="block text-sm font-medium text-gray-700">
            Industry Template
          </label>
          <select
            id="template"
            name="template"
            value={formData.template}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="ecommerce">E-commerce</option>
            <option value="legal">Legal Services</option>
            <option value="realestate">Real Estate</option>
            <option value="healthcare">Healthcare</option>
            <option value="fintech">Financial Technology</option>
          </select>
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

      {/* Progress display */}
      {isGenerating && (
        <div className="mt-6">
          <h3 className="text-lg font-medium text-gray-900 mb-2">Progress</h3>
          <div className="bg-gray-50 p-4 rounded-md">
            {progress.map((item, index) => (
              <div key={index} className="mb-2">
                {item.type === 'start' && (
                  <p className="text-blue-600">▶ Starting: {item.command}</p>
                )}
                {item.type === 'output' && (
                  <p className={item.stream === 'stderr' ? 'text-red-600' : 'text-gray-600'}>
                    {item.data}
                  </p>
                )}
                {item.type === 'complete' && (
                  <p className="text-green-600">✅ Completed with exit code {item.exit_code}</p>
                )}
                {item.type === 'error' && (
                  <p className="text-red-600">❌ Error: {item.message}</p>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </form>
  );
}