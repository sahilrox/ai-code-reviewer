import { Review } from '@/lib/api'

interface Stat {
  label: string
  value: number | string
  icon: string
  color: string
}

export default function StatsBar({ reviews }: { reviews: Review[] }) {
  const totalReviews = reviews.length
  const totalErrors = reviews.reduce((s, r) => s + r.error_count, 0)
  const totalWarnings = reviews.reduce((s, r) => s + r.warning_count, 0)
  const avgComments = totalReviews
    ? (reviews.reduce((s, r) => s + r.comment_count, 0) / totalReviews).toFixed(1)
    : 0

  const stats: Stat[] = [
    { label: 'Total Reviews', value: totalReviews, icon: '🔍', color: '#6366f1' },
    { label: 'Errors Caught', value: totalErrors, icon: '🔴', color: '#ef4444' },
    { label: 'Warnings', value: totalWarnings, icon: '🟡', color: '#f59e0b' },
    { label: 'Avg Comments / PR', value: avgComments, icon: '💬', color: '#10b981' },
  ]

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {stats.map((stat) => (
        <div
          key={stat.label}
          className="bg-gray-900 border border-gray-800 rounded-xl p-5 flex flex-col gap-2"
        >
          <div className="text-2xl">{stat.icon}</div>
          <div className="text-3xl font-bold" style={{ color: stat.color }}>
            {stat.value}
          </div>
          <div className="text-sm text-gray-400">{stat.label}</div>
        </div>
      ))}
    </div>
  )
}