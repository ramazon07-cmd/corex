export default function ResultDisplay({ result }) {
  if (!result) return null;

  return (
    <div className={`mt-6 p-4 rounded-md ${result.success ? 'bg-green-50' : 'bg-red-50'}`}>
      <div className="flex">
        <div className="flex-shrink-0">
          {result.success ? (
            <svg className="h-5 w-5 text-green-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
          )}
        </div>
        <div className="ml-3">
          <h3 className={`text-sm font-medium ${result.success ? 'text-green-800' : 'text-red-800'}`}>
            {result.message}
          </h3>
          {result.command && (
            <div className="mt-2 text-sm text-green-700">
              <p>Command executed:</p>
              <pre className="mt-1 p-2 bg-green-100 rounded-md overflow-x-auto">
                <code>{result.command}</code>
              </pre>
            </div>
          )}
          {result.error && (
            <div className="mt-2 text-sm text-red-700">
              <p>Error details:</p>
              <p className="mt-1">{result.error}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}