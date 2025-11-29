import { useState } from 'react';
import Head from 'next/head';
import ProjectForm from '../components/ProjectForm';
import AppForm from '../components/AppForm';
import ResultDisplay from '../components/ResultDisplay';

export default function Home() {
  const [activeTab, setActiveTab] = useState('project');
  const [isGenerating, setIsGenerating] = useState(false);
  const [result, setResult] = useState(null);

  const handleProjectResult = (result) => {
    setIsGenerating(false);
    setResult(result);
  };

  const handleAppResult = (result) => {
    setIsGenerating(true);
    setResult(result);
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>CoreX GUI - Django Scaffolding Framework</title>
        <meta name="description" content="Graphical interface for CoreX Django scaffolding framework" />
      </Head>

      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">CoreX GUI</h1>
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-500">Django Scaffolding Framework</span>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="border-b border-gray-200">
              <nav className="-mb-px flex space-x-8" aria-label="Tabs">
                <button
                  onClick={() => setActiveTab('project')}
                  className={`${
                    activeTab === 'project'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
                >
                  New Project
                </button>
                <button
                  onClick={() => setActiveTab('app')}
                  className={`${
                    activeTab === 'app'
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm`}
                >
                  New App
                </button>
              </nav>
            </div>

            <div className="p-6">
              {activeTab === 'project' && (
                <ProjectForm onSubmit={handleProjectResult} isGenerating={isGenerating} />
              )}

              {activeTab === 'app' && (
                <AppForm onSubmit={handleAppResult} isGenerating={isGenerating} />
              )}

              <ResultDisplay result={result} />
            </div>
          </div>

          <div className="mt-8 bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6">
              <h3 className="text-lg leading-6 font-medium text-gray-900">About CoreX</h3>
              <p className="mt-1 max-w-2xl text-sm text-gray-500">
                A comprehensive Django scaffolding framework for rapid development.
              </p>
            </div>
            <div className="border-t border-gray-200 px-4 py-5 sm:p-0">
              <dl className="sm:divide-y sm:divide-gray-200">
                <div className="py-4 sm:py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                  <dt className="text-sm font-medium text-gray-500">Features</dt>
                  <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                    <ul className="border border-gray-200 rounded-md divide-y divide-gray-200">
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            Specialized app templates (Blog, Shop, Wiki, CRM, etc.)
                          </span>
                        </div>
                      </li>
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            Authentication options (Session, JWT, Allauth)
                          </span>
                        </div>
                      </li>
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            UI frameworks (Tailwind CSS, Bootstrap)
                          </span>
                        </div>
                      </li>
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            Database support (SQLite, PostgreSQL, MySQL)
                          </span>
                        </div>
                      </li>
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            Docker integration
                          </span>
                        </div>
                      </li>
                      <li className="pl-3 pr-4 py-3 flex items-center justify-between text-sm">
                        <div className="w-0 flex-1 flex items-center">
                          <span className="ml-2 flex-1 w-0 truncate">
                            API generation with Django REST Framework
                          </span>
                        </div>
                      </li>
                    </ul>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>
      </main>

      <footer className="bg-white">
        <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-gray-500">
            CoreX GUI - Django Scaffolding Framework
          </p>
        </div>
      </footer>
    </div>
  );
}