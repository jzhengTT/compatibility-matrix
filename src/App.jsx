import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ModelGrid from './components/ModelGrid'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({
    tasks: [],
    models: [],
    hardware: [],
    software: [],
    status: []
  })

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex">
        {/* Sidebar */}
        <div className="w-80 bg-white border-r border-gray-200 min-h-screen">
          <Sidebar
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
            filters={filters}
            onFilterChange={setFilters}
          />
        </div>

        {/* Main Content */}
        <div className="flex-1">
          <ModelGrid
            searchQuery={searchQuery}
            filters={filters}
          />
        </div>
      </div>
    </div>
  )
}

export default App
