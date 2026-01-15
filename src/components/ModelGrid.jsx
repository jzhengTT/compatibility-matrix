import { useState, useEffect } from 'react'
import ModelCard from './ModelCard'
import modelsData from '../../docs/supported-models.json'

const ModelGrid = ({ searchQuery, filters }) => {
  const [filteredModels, setFilteredModels] = useState([])

  useEffect(() => {
    // Apply filters and search
    let filtered = modelsData.Models || []

    // Apply search query
    if (searchQuery.trim()) {
      const query = searchQuery.toLowerCase()
      filtered = filtered.filter(model =>
        model.DisplayName.toLowerCase().includes(query) ||
        model.Family.toLowerCase().includes(query) ||
        model.Tasks.some(task => task.toLowerCase().includes(query)) ||
        model.Description.toLowerCase().includes(query)
      )
    }

    // Apply task filters
    if (filters.tasks.length > 0) {
      filtered = filtered.filter(model =>
        model.Tasks.some(task => filters.tasks.includes(task))
      )
    }

    // Apply model family filters
    if (filters.models.length > 0) {
      filtered = filtered.filter(model =>
        filters.models.includes(model.Family)
      )
    }

    // Apply hardware filters
    if (filters.hardware.length > 0) {
      filtered = filtered.filter(model =>
        model.Variants.some(variant =>
          variant.CompatibilityList.some(comp =>
            filters.hardware.includes(comp.SupportedHardware)
          )
        )
      )
    }

    // Apply status filters - Note: new schema doesn't have status field
    // This filter will be inactive with the current supported-models.json structure
    if (filters.status.length > 0) {
      // Since the new schema doesn't have status, we'll keep all models
      // This could be extended if status information is added to the new schema
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