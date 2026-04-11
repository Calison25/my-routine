export const DEFAULT_API_URL = 'http://localhost:8001'
const BASE_URL = import.meta.env.VITE_API_URL || DEFAULT_API_URL

class ApiError extends Error {
  statusCode: number

  constructor(statusCode: number, message: string) {
    super(message)
    this.statusCode = statusCode
  }
}

async function apiRequest<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  const body = await response.json()
  if (!response.ok) {
    throw new ApiError(response.status, body.error || 'Erro desconhecido')
  }
  return body.data
}

export { apiRequest, ApiError }
