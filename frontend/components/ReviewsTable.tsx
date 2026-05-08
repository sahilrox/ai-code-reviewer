'use client'
import {
  LineChart, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, PieChart, Pie,
  Cell, Legend, BarChart, Bar
} from 'recharts'
import { Review } from '@/lib/api'

function getLineData(reviews: Review[]) {
  const byDate: Record<string, number> = {}
  reviews.forEach((r) => {
    const date = new Date(r.timestamp).toLocaleDateString('en-US', {
      month: 'short', day: 'numeric'
    })
    byDate[date] = (byDate[date] || 0) + 1
  })
  return Object.entries(byDate).map(([date, count]) => ({ date, reviews: count }))
}

function getSeverityData(reviews: Review[]) {
  return [
    { name: 'Errors', value: reviews.reduce((s, r) => s + r.error_count, 0), color: '#ef4444' },
    { name: 'Warnings', value: reviews.reduce((s, r) => s + r.warning_count, 0), color: '#f59e0b' },
    { name: 'Suggestions', value: reviews.reduce((s, r) => s + r.suggestion_count, 0), color: '#6366f1' },
  ]
}

function getAuthorData(reviews: Review[]) {
  const byAuthor: Record<string, number> = {}
  reviews.forEach((r) => {
    byAuthor[r.author] = (byAuthor[r.author] || 0) + r.comment_count
  })
  return Object.entries(byAuthor)
    .map(([author, comments]) => ({ author, comments }))
    .sort((a, b) => b.comments - a.comments)
    .slice(0, 8)
}

export default function Charts({ reviews }: { reviews: Review[] }) {
  const lineData = getLineData(reviews)
  const severityData = getSeverityData(reviews)
  const authorData = getAuthorData(reviews)

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">

      {/* Reviews Over Time */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-4">
          Reviews Over Time
        </h2>
        <ResponsiveContainer width="100%" height={220}>
          <LineChart data={lineData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="date" stroke="#6b7280" tick={{ fontSize: 11 }} />
            <YAxis stroke="#6b7280" tick={{ fontSize: 11 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
              labelStyle={{ color: '#f9fafb' }}
            />
            <Line
              type="monotone" dataKey="reviews"
              stroke="#6366f1" strokeWidth={2}
              dot={{ fill: '#6366f1', r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Severity Breakdown */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-4">
          Severity Breakdown
        </h2>
        <ResponsiveContainer width="100%" height={220}>
          <PieChart>
            <Pie
              data={severityData} cx="50%" cy="50%"
              innerRadius={60} outerRadius={90}
              paddingAngle={4} dataKey="value"
            >
              {severityData.map((entry, i) => (
                <Cell key={i} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
            />
            <Legend
              iconType="circle"
              formatter={(value) => <span style={{ color: '#9ca3af', fontSize: 12 }}>{value}</span>}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Comments by Author */}
      <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 md:col-span-2">
        <h2 className="text-sm font-semibold text-gray-400 uppercase tracking-widest mb-4">
          Comments by Author
        </h2>
        <ResponsiveContainer width="100%" height={220}>
          <BarChart data={authorData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
            <XAxis dataKey="author" stroke="#6b7280" tick={{ fontSize: 11 }} />
            <YAxis stroke="#6b7280" tick={{ fontSize: 11 }} />
            <Tooltip
              contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: 8 }}
              labelStyle={{ color: '#f9fafb' }}
            />
            <Bar dataKey="comments" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>

    </div>
  )
}