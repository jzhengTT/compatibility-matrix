const ModelCard = ({ model }) => {
  const getSupportedHardware = () => {
    return model.compatibility
      .filter(comp => comp.status === 'Supported')
      .map(comp => comp.hardware)
  }

  const getPerformanceMetrics = () => {
    return model.compatibility
      .filter(comp => comp.status === 'Supported' && comp.metrics)
      .map(comp => ({
        hardware: comp.hardware,
        metrics: comp.metrics
      }))
  }

  const supportedHardware = getSupportedHardware()
  const performanceMetrics = getPerformanceMetrics()

  return (
    <div className="bg-white rounded-lg border border-gray-200 hover:shadow-lg transition-all duration-200 hover:border-gray-300">
      {/* Card Header */}
      <div className="p-4 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {model.display_name}
        </h3>
        <div className="flex items-center gap-2 mb-3">
          <span className="text-sm text-gray-600">{model.family}</span>
          <div className="flex flex-wrap gap-1">
            {model.tasks.map((task) => (
              <span
                key={task}
                className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
              >
                {task}
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Card Body */}
      <div className="p-4">
        {/* Supported Hardware */}
        {supportedHardware.length > 0 ? (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Supported Hardware</h4>
            <div className="flex flex-wrap gap-1">
              {supportedHardware.slice(0, 3).map((hardware) => (
                <span
                  key={hardware}
                  className="inline-flex items-center px-2 py-1 rounded text-xs bg-green-50 text-green-700 border border-green-200"
                >
                  {hardware}
                </span>
              ))}
              {supportedHardware.length > 3 && (
                <span className="text-xs text-gray-500 px-2 py-1">
                  +{supportedHardware.length - 3} more
                </span>
              )}
            </div>
          </div>
        ) : (
          <div className="mb-4">
            <span className="text-xs text-gray-500">No supported hardware yet</span>
          </div>
        )}

        {/* Performance Metrics */}
        {performanceMetrics.length > 0 && (
          <div className="mb-2">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Performance Metrics</h4>
            <div className="space-y-2">
              {performanceMetrics.slice(0, 1).map((item, index) => (
                <div key={index} className="text-xs bg-gray-50 p-2 rounded">
                  <div className="font-medium text-gray-700 mb-1">{item.hardware}</div>
                  <div className="space-y-0.5 text-gray-600">
                    {item.metrics.mean_tps && (
                      <div>TPS: {item.metrics.mean_tps.toFixed(2)}</div>
                    )}
                    {item.metrics.mean_ttft_ms && (
                      <div>TTFT: {item.metrics.mean_ttft_ms.toFixed(1)}ms</div>
                    )}
                    {item.metrics.ttft && (
                      <div>TTFT: {item.metrics.ttft}ms</div>
                    )}
                    {item.metrics.accuracy_check !== undefined && (
                      <div>Accuracy: {item.metrics.accuracy_check ? '✓' : '✗'}</div>
                    )}
                  </div>
                </div>
              ))}
              {performanceMetrics.length > 1 && (
                <div className="text-xs text-gray-500">
                  +{performanceMetrics.length - 1} more hardware configuration{performanceMetrics.length - 1 !== 1 ? 's' : ''}
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default ModelCard