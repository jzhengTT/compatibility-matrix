import SearchInput from './SearchInput'
import FilterSection from './FilterSection'

const Sidebar = ({ searchQuery, onSearchChange, filters, onFilterChange }) => {

  const handleFilterChange = (filterType, value, checked) => {
    const newFilters = { ...filters }
    if (checked) {
      newFilters[filterType] = [...newFilters[filterType], value]
    } else {
      newFilters[filterType] = newFilters[filterType].filter(item => item !== value)
    }
    onFilterChange(newFilters)
  }

  const filterSections = [
    {
      name: 'Task',
      key: 'tasks',
      displayType: 'pills',
      options: ['LLM', 'Vision', 'Text-Generation', 'Image-Classification', 'Text-to-Image', 'Image-Generation', 'Image-Segmentation']
    },
    {
      name: 'Model Family',
      key: 'models',
      displayType: 'pills',
      options: ['LLaMA', 'Qwen', 'Gemma', 'Mistral', 'ResNet', 'EfficientNet', 'MobileNet', 'ViT', 'VoVNet', 'SegFormer', 'UNet']
    },
    {
      name: 'Hardware',
      key: 'hardware',
      displayType: 'hardware',
      options: [
        'Galaxy (Wormhole)',
        'n150 (Wormhole)',
        'n300 (Wormhole)',
        'Quietbox (Blackhole)',
        'Loudbox (Wormhole)',
        'p100 (Blackhole)'
      ]
    },
    {
      name: 'Status',
      key: 'status',
      displayType: 'status',
      options: ['Supported', 'Not Supported']
    }
  ]

  return (
    <div className="h-full flex flex-col">
      {/* Search Section */}
      <div className="p-4 border-b border-gray-200">
        <SearchInput
          value={searchQuery}
          onChange={onSearchChange}
          placeholder="Search for a model, hardware, etc"
        />
      </div>

      {/* Filter Sections */}
      <div className="flex-1 overflow-y-auto">
        {filterSections.map((section) => (
          <FilterSection
            key={section.key}
            name={section.name}
            options={section.options}
            selectedValues={filters[section.key]}
            displayType={section.displayType}
            onFilterChange={(value, checked) => handleFilterChange(section.key, value, checked)}
          />
        ))}
      </div>
    </div>
  )
}

export default Sidebar