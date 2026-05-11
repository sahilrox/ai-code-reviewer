import axios from 'axios'

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export interface Review {
  id: string
  repo: string
  pr_number: number
  author: string
  title: string
  comment_count: number
  error_count: number
  warning_count: number
  suggestion_count: number
  timestamp: string
}

export interface ReviewsResponse {
  reviews: Review[]
}

export const fetchReviews = async (): Promise<Review[]> => {
  console.log('Fetching from:', API_BASE)
  const { data } = await axios.get<ReviewsResponse>(`${API_BASE}/reviews`, {
    timeout: 10000,
    headers: {
      'Content-Type': 'application/json',
    }
  })
  console.log('Got reviews:', data.reviews.length)
  return data.reviews
}