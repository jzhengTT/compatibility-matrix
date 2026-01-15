const ModelCard = ({ model }) => {
  const getHardwareDisplayName = (hardwareValue) => {
    const hardwareMap = {
      'galaxy': 'Galaxy (Blackhole)'
    }
    return hardwareMap[hardwareValue] || hardwareValue
  }

  const getSupportedHardware = () => {
    const hardware = new Set()
    model.Variants.forEach(variant => {
      variant.CompatibilityList.forEach(comp => {
        // Note: new schema doesn't have status field, assuming all are supported
        hardware.add(comp.SupportedHardware)
      })
    })
    return Array.from(hardware).map(hw => getHardwareDisplayName(hw))
  }

  const getVariantInfo = () => {
    return model.Variants.map(variant => ({
      name: variant.DisplayName,
      parameters: 'N/A', // New schema doesn't have parameters field
      precision: variant.Precision || 'N/A'
    }))
  }

  const supportedHardware = getSupportedHardware()
  const variants = getVariantInfo()

  return (
    <div className="bg-white rounded-lg border border-gray-200 hover:shadow-lg transition-all duration-200 hover:border-gray-300">
      {/* Card Header */}
      <div className="p-4 border-b border-gray-100">
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {model.DisplayName}
        </h3>
        <div className="flex flex-wrap gap-1 mb-3">
          {model.Tasks.map((task) => (
            <span
              key={task}
              className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-50 text-blue-700 border border-blue-200"
            >
              {task}
            </span>
          ))}
        </div>
        <p className="text-sm text-gray-600 line-clamp-2">
          {model.Description}
        </p>
      </div>

      {/* Card Body */}
      <div className="p-4">
        {/* Variants */}
        {variants.length > 0 && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Variants</h4>
            <div className="space-y-1">
              {variants.slice(0, 2).map((variant, index) => (
                <div key={index} className="text-xs text-gray-600">
                  {variant.name} • {variant.parameters} • {variant.precision}
                </div>
              ))}
              {variants.length > 2 && (
                <div className="text-xs text-gray-500">
                  +{variants.length - 2} more variant{variants.length - 2 !== 1 ? 's' : ''}
                </div>
              )}
            </div>
          </div>
        )}

        {/* Supported Hardware */}
        {supportedHardware.length > 0 && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Supported Hardware</h4>
            <div className="flex flex-wrap gap-1">
              {supportedHardware.slice(0, 2).map((hardware) => (
                <span
                  key={hardware}
                  className="inline-flex items-center px-2 py-1 rounded text-xs bg-gray-100 text-gray-700"
                >
                  {hardware}
                </span>
              ))}
              {supportedHardware.length > 2 && (
                <span className="text-xs text-gray-500 px-2 py-1">
                  +{supportedHardware.length - 2} more
                </span>
              )}
            </div>
          </div>
        )}

        {/* Editorial Notes */}
        {model.EditorialNotes && model.EditorialNotes.trim() && (
          <div className="mb-4">
            <h4 className="text-sm font-medium text-gray-900 mb-2">Notes</h4>
            <p className="text-xs text-gray-600">
              {model.EditorialNotes}
            </p>
          </div>
        )}
      </div>

      {/* Card Footer */}
      <div className="px-4 pb-4">
        {model.Links && model.Links.length > 0 && (
          <div className="flex space-x-2">
            {model.Links.map((link, index) => (
              <a
                key={index}
                href={link}
                target="_blank"
                rel="noopener noreferrer"
                className="text-xs text-blue-600 hover:text-blue-800"
              >
                Link {index + 1}
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ModelCard