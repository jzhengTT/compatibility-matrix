const LoadingState = () => {
  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Models
        </h1>
      </div>

      <div className="flex items-center justify-center py-12">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mb-4"></div>
          <h3 className="text-sm font-medium text-gray-900 mb-1">Loading compatibility data</h3>
          <p className="text-sm text-gray-500">
            Please wait while we fetch the latest model compatibility information...
          </p>
        </div>
      </div>
    </div>
  )
}

export default LoadingState
