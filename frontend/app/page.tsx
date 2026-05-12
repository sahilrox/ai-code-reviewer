'use client'
import { useEffect, useState, useCallback } from 'react'
import { fetchReviews, Review } from '@/lib/api'
import StatsBar from '@/components/StatsBar'
import Charts from '@/components/Charts'
import ReviewsTable from '@/components/ReviewsTable'

export default function Dashboard() {
  const [reviews, setReviews] = useState<Review[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  const loadReviews = useCallback(async () => {
    try {
      const data = await fetchReviews()
      setReviews(data)
      setLastUpdated(new Date())
      setError('')
    } catch {
      setError('Could not connect to backend — make sure uvicorn is running on port 8000')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    let cancelled = false

    const load = async () => {
      try {
        const data = await fetchReviews()
        if (!cancelled) {
          setReviews(data)
          setLastUpdated(new Date())
          setError('')
          setLoading(false)
        }
      } catch {
        if (!cancelled) {
          setError('Could not connect to backend — make sure uvicorn is running on port 8000')
          setLoading(false)
        }
      }
    }

    load()

    // Auto-refresh every 30 seconds
    const interval = setInterval(() => {
      if (!cancelled) loadReviews()
    }, 30000)

    return () => {
      cancelled = true
      clearInterval(interval)
    }
  }, [loadReviews])

  return (
    <main className="min-h-screen bg-gray-950 text-white">

      {/* Header */}
      <div className="border-b border-gray-800 bg-gray-950 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <span className="text-2xl">🤖</span>
            <div>
              <h1 className="text-lg font-bold text-white">AI Code Reviewer</h1>
              <p className="text-xs text-gray-500">Review analytics dashboard</p>
            </div>
          </div>
          <div className="flex items-center gap-4">
            {lastUpdated && (
              <span className="text-xs text-gray-600">
                Updated {lastUpdated.toLocaleTimeString()}
              </span>
            )}
            <button
              onClick={loadReviews}
              className="text-xs bg-gray-800 hover:bg-gray-700 text-gray-300 px-3 py-1.5 rounded-lg transition-colors"
            >
              ↻ Refresh
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">

        {/* Error Banner */}
        {error && (
          <div className="bg-red-950 border border-red-800 text-red-300 rounded-xl px-5 py-4 mb-6 text-sm">
            ⚠️ {error}
          </div>
        )}

        {/* Loading State */}
        {loading ? (
          <div className="flex items-center justify-center h-64 text-gray-600">
            Loading reviews...
          </div>
        ) : (
          <>
            <StatsBar reviews={reviews} />
            <Charts reviews={reviews} />
            <ReviewsTable reviews={reviews} />
          </>
        )}

      </div>
    </main>
  ) 
} 