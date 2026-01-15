import GlobeIcon from './GlobeIcon'

const FilterSection = ({
  name,
  options,
  selectedValues,
  onFilterChange,
  displayType = 'checkbox'
}) => {
  const getModelIcon = (model) => {
    const icons = {
      'Llama': '🦙',
      'LlaMA': '🦙',
      'DeepSeek': '🔍',
      'Qwen': '🟦',
      'Falcon': '🦅'
    }
    return icons[model] || '🤖'
  }

  const getSoftwareIcon = (software) => {
    const icons = {
      'TT-Forge': '🔥',
      'TT-NN': '🧠',
      'TT-Metallium': '⚡',
      'TT-LLK': '📚'
    }
    return icons[software] || '💻'
  }

  const getHardwareInfo = (hardware) => {
    if (hardware.includes('Blackhole')) {
      return { label: hardware.replace(' (Blackhole)', ''), badge: 'BLACKHOLE', color: 'bg-black text-white' }
    }
    if (hardware.includes('Wormhole')) {
      return { label: hardware.replace(' (Wormhole)', ''), badge: 'WORMHOLE', color: 'bg-purple-600 text-white' }
    }
    return { label: hardware, badge: '', color: '' }
  }

  const getStatusColor = (status) => {
    const colors = {
      'Supported': 'bg-green-500',
      'Coming Soon': 'bg-blue-500',
      'Deprecated': 'bg-gray-400'
    }
    return colors[status] || 'bg-gray-400'
  }

  const renderTaskButtons = () => (
    <div className="flex flex-wrap gap-2 px-4 pb-3">
      {options.map((option) => {
        const isSelected = selectedValues.includes(option)
        return (
          <button
            key={option}
            onClick={() => onFilterChange(option, !isSelected)}
            className={`px-3 py-1.5 text-xs font-medium rounded-full transition-colors ${
              isSelected
                ? 'bg-blue-100 text-blue-800 border border-blue-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            {option}
          </button>
        )
      })}
    </div>
  )

  const renderModelPills = () => (
    <div className="flex flex-wrap gap-2 px-4 pb-3">
      {options.map((option) => {
        const isSelected = selectedValues.includes(option)
        return (
          <button
            key={option}
            onClick={() => onFilterChange(option, !isSelected)}
            className={`flex items-center gap-2 px-3 py-1.5 text-xs font-medium rounded-full transition-colors ${
              isSelected
                ? 'bg-blue-100 text-blue-800 border border-blue-200'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <GlobeIcon className="w-3 h-3" />
            {option}
          </button>
        )
      })}
    </div>
  )

  const renderModelItems = () => (
    <div className="px-4 pb-3 space-y-2">
      {options.map((option) => {
        const isSelected = selectedValues.includes(option)
        return (
          <button
            key={option}
            onClick={() => onFilterChange(option, !isSelected)}
            className={`w-full flex items-center space-x-3 text-sm cursor-pointer hover:bg-gray-50 px-2 py-2 rounded ${
              isSelected ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
            }`}
          >
            <span className="text-lg">{getModelIcon(option)}</span>
            <span className={`${isSelected ? 'font-medium' : ''}`}>{option}</span>
          </button>
        )
      })}
    </div>
  )

  const renderHardwareItems = () => (
    <div className="px-4 pb-3 space-y-2">
      {options.map((option) => {
        // Handle both string and object formats
        const optionValue = typeof option === 'object' ? option.value : option
        const optionLabel = typeof option === 'object' ? option.label : option
        const isSelected = selectedValues.includes(optionValue)
        const { label, badge, color } = getHardwareInfo(optionLabel)
        return (
          <button
            key={optionValue}
            onClick={() => onFilterChange(optionValue, !isSelected)}
            className={`w-full flex items-center justify-between text-sm cursor-pointer hover:bg-gray-50 px-2 py-2 rounded ${
              isSelected ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
            }`}
          >
            <div className="flex items-center space-x-2">
              <span>📱</span>
              <span className={`${isSelected ? 'font-medium' : ''}`}>{label}</span>
            </div>
            {badge && (
              <span className={`text-xs px-2 py-0.5 rounded ${color}`}>
                {badge}
              </span>
            )}
          </button>
        )
      })}
    </div>
  )

  const renderSoftwareItems = () => (
    <div className="px-4 pb-3 space-y-2">
      {options.map((option) => {
        const isSelected = selectedValues.includes(option)
        return (
          <button
            key={option}
            onClick={() => onFilterChange(option, !isSelected)}
            className={`w-full flex items-center space-x-3 text-sm cursor-pointer hover:bg-gray-50 px-2 py-2 rounded ${
              isSelected ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
            }`}
          >
            <span className="text-lg">{getSoftwareIcon(option)}</span>
            <span className={`${isSelected ? 'font-medium' : ''}`}>{option}</span>
          </button>
        )
      })}
    </div>
  )

  const renderStatusItems = () => (
    <div className="px-4 pb-3 space-y-2">
      {options.map((option) => {
        const isSelected = selectedValues.includes(option)
        return (
          <button
            key={option}
            onClick={() => onFilterChange(option, !isSelected)}
            className={`w-full flex items-center space-x-3 text-sm cursor-pointer hover:bg-gray-50 px-2 py-2 rounded ${
              isSelected ? 'bg-blue-50 text-blue-900' : 'text-gray-700'
            }`}
          >
            <div className={`w-3 h-3 rounded-full ${getStatusColor(option)}`}></div>
            <span className={`${isSelected ? 'font-medium' : ''}`}>{option}</span>
          </button>
        )
      })}
    </div>
  )

  const renderContent = () => {
    switch (displayType) {
      case 'pills':
        // Check if this is the Models section to render with globe icons
        if (name === 'Models') {
          return renderModelPills()
        }
        return renderTaskButtons()
      case 'models':
        return renderModelItems()
      case 'hardware':
        return renderHardwareItems()
      case 'software':
        return renderSoftwareItems()
      case 'status':
        return renderStatusItems()
      default:
        return renderModelItems()
    }
  }

  return (
    <div className="border-b border-gray-200">
      {/* Section Header - No longer collapsible */}
      <div className="px-4 py-3 text-sm font-medium text-gray-900">
        {name}
      </div>

      {/* Section Content - Always visible */}
      {renderContent()}
    </div>
  )
}

export default FilterSection