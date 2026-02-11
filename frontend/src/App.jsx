import { useState } from 'react'
import Sidebar from './components/Sidebar'
import ModelGrid from './components/ModelGrid'
import { useCompatibilityData } from './hooks/useCompatibilityData'

function App() {
  const [searchQuery, setSearchQuery] = useState('')
  const [filters, setFilters] = useState({
    tasks: [],
    models: [],
    hardware: [],
    software: [],
    status: []
  })

  // Fetch compatibility data from backend API
  const { data: compatibilityData, loading, error, refetch } = useCompatibilityData()

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
            compatibilityData={compatibilityData}
            loading={loading}
            error={error}
            onRetry={refetch}
            searchQuery={searchQuery}
            filters={filters}
          />
        </div>
      </div>
    </div>
  )
}

export default App
