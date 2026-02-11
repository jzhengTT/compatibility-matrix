import { useState, useEffect } from 'react'

/**
 * Custom hook to fetch compatibility data from the backend API
 * @returns {Object} { data, loading, error, refetch }
 */
export function useCompatibilityData() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)

      const apiUrl = import.meta.env.VITE_API_URL || '/api/compatibility'
      const response = await fetch(apiUrl)

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`)
      }

      const json = await response.json()
      setData(json)
    } catch (err) {
      console.error('Error fetching compatibility data:', err)
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
  }, [])

  return {
    data,
    loading,
    error,
    refetch: fetchData
  }
}
