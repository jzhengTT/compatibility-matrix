import { useState, useEffect } from 'react'
import ModelCard from './ModelCard'
import compatibilityData from '../../data/compatibility.json'

const ModelGrid = ({ searchQuery, filters }) => {
  const [filteredModels, setFilteredModels] = useState([])

  useEffect(() => {
    // Apply filters and search
    let filtered = compatibilityData.models || []

    // Apply search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(model =>
        model.display_name.toLowerCase().includes(query) ||
        model.family.toLowerCase().includes(query) ||
        model.tasks.some(task => task.toLowerCase().includes(query))
      )
    }

    // Apply task filters
    if (filters.tasks.length > 0) {
      filtered = filtered.filter(model =>
        model.tasks.some(task => filters.tasks.includes(task))
      )
    }

    // Apply model family filters
    if (filters.models.length > 0) {
      filtered = filtered.filter(model =>
        filters.models.includes(model.family)
      )
    }

    // Apply hardware filters - only show models that are SUPPORTED on the selected hardware
    if (filters.hardware.length > 0) {
      filtered = filtered.filter(model =>
        model.compatibility.some(comp =>
          filters.hardware.includes(comp.hardware) && comp.status === 'Supported'
        )
      )
    }

    // Apply status filters
    if (filters.status.length > 0) {
      filtered = filtered.filter(model =>
        model.compatibility.some(comp =>
          filters.status.includes(comp.status)
        )
      )
    }

    setFilteredModels(filtered)
  }, [searchQuery, filters])

  const totalModels = filteredModels.length

  return (
    <div className="p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-2xl font-bold text-gray-900">
          Models{' '}
          <span className="text-sm font-normal text-gray-500">
            {totalModels} model{totalModels !== 1 ? 's' : ''}
          </span>
        </h1>
      </div>

      {/* Models Grid */}
      {totalModels === 0 ? (
        <div className="text-center py-12">
          <div className="text-gray-400 mb-4">
            <svg className="mx-auto h-12 w-12" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-2.34 0-4.29-1.009-5.824-2.562M15 6.306A7.962 7.962 0 0112 5c-2.34 0-4.29 1.009-5.824 2.562" />
            </svg>
          </div>
          <h3 className="text-sm font-medium text-gray-900 mb-1">No models found</h3>
          <p className="text-sm text-gray-500">
            Try adjusting your search query or filters to find what you're looking for.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-6">
          {filteredModels.map((model) => (
            <ModelCard key={model.id} model={model} />
          ))}
        </div>
      )}
    </div>
  )
}

export default ModelGrid