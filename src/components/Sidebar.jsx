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
      options: ['text-generation', 'image-generation', 'speech-recognition']
    },
    {
      name: 'Models',
      key: 'models',
      displayType: 'pills',
      options: ['Qwen', 'Gemma', 'Llama', 'Stable Diffusion', 'Whisper']
    },
    {
      name: 'Supported Hardware',
      key: 'hardware',
      displayType: 'hardware',
      options: [
        { value: 'galaxy', label: 'Galaxy (Blackhole)' }
      ]
    },
    // Note: Commented out software and status filters as new schema doesn't have this data
    // {
    //   name: 'Supported Software',
    //   key: 'software',
    //   displayType: 'software',
    //   options: ['TT-Forge', 'TT-NN', 'TT-Metallium', 'TT-LLK']
    // },
    // {
    //   name: 'Status',
    //   key: 'status',
    //   displayType: 'status',
    //   options: ['Supported', 'Coming Soon', 'Deprecated']
    // }
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