import { useState } from 'react';

export default function AppForm({ onSubmit, isGenerating }) {
  const [formData, setFormData] = useState({
    appName: '',
    type: 'blog',
    auth: '',
    ui: '',
    seed: false,
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
      const response = await fetch('/api/create-app', {
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
        message: 'Failed to create app',
        error: error.message
      });
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Create New Django App</h2>
        <p className="text-gray-600 mb-6">
          Generate a specialized Django app with pre-built models and features.
        </p>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div>
          <label htmlFor="appName" className="block text-sm font-medium text-gray-700">
            App Name
          </label>
          <input
            type="text"
            name="appName"
            id="appName"
            value={formData.appName}
            onChange={handleChange}
            required
            className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            placeholder="blog"
          />
        </div>

        <div>
          <label htmlFor="type" className="block text-sm font-medium text-gray-700">
            App Type
          </label>
          <select
            id="type"
            name="type"
            value={formData.type}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="blog">Blog (Posts, Comments)</option>
            <option value="shop">Shop (Products, Orders)</option>
            <option value="wiki">Wiki (Pages, Revisions)</option>
            <option value="crm">CRM (Contacts, Deals)</option>
            <option value="social">Social (Profiles, Posts)</option>
            <option value="forum">Forum (Topics, Posts)</option>
            <option value="portfolio">Portfolio (Projects, Skills)</option>
            <option value="elearn">E-learning (Courses, Lessons)</option>
            <option value="education">Education (Students, Courses)</option>
            <option value="fintech">Fintech (Accounts, Transactions)</option>
            <option value="healthcare">Healthcare (Patients, Records)</option>
          </select>
        </div>

        <div>
          <label htmlFor="appAuth" className="block text-sm font-medium text-gray-700">
            Authentication Override
          </label>
          <select
            id="appAuth"
            name="auth"
            value={formData.auth}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="">Use Project Default</option>
            <option value="session">Session</option>
            <option value="jwt">JWT</option>
            <option value="allauth">Allauth</option>
          </select>
        </div>

        <div>
          <label htmlFor="appUi" className="block text-sm font-medium text-gray-700">
            UI Framework Override
          </label>
          <select
            id="appUi"
            name="ui"
            value={formData.ui}
            onChange={handleChange}
            className="mt-1 block w-full bg-white border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
          >
            <option value="">Use Project Default</option>
            <option value="tailwind">Tailwind CSS</option>
            <option value="bootstrap">Bootstrap</option>
            <option value="none">None</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div className="flex items-center">
          <input
            id="seed"
            name="seed"
            type="checkbox"
            checked={formData.seed}
            onChange={handleChange}
            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label htmlFor="seed" className="ml-2 block text-sm text-gray-900">
            Generate Demo Data
          </label>
        </div>

        <div className="flex items-center">
          <input
            id="appApi"
            name="api"
            type="checkbox"
            checked={formData.api}
            onChange={handleChange}
            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
          />
          <label htmlFor="appApi" className="ml-2 block text-sm text-gray-900">
            Include API Endpoints
          </label>
        </div>
      </div>

      <div className="flex justify-end">
        <button
          type="submit"
          disabled={isGenerating || !formData.appName}
          className={`inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white ${
            isGenerating || !formData.appName
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500'
          }`}
        >
          {isGenerating ? 'Creating...' : 'Create App'}
        </button>
      </div>
    </form>
  );
}