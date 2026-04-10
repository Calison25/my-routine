import { describe, it, expect, vi, beforeEach } from 'vitest'

describe('apiRequest', () => {
  beforeEach(() => {
    vi.restoreAllMocks()
  })

  it('should return data on successful response', async () => {
    const mockData = [{ id: 1, name: 'Musculação' }]

    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: true,
        json: () => Promise.resolve({ data: mockData }),
      }),
    )

    const { apiRequest } = await import('./api-client')
    const result = await apiRequest('/api/categories')

    expect(fetch).toHaveBeenCalledWith(
      'http://localhost:8001/api/categories',
      expect.objectContaining({
        headers: { 'Content-Type': 'application/json' },
      }),
    )
    expect(result).toEqual(mockData)
  })

  it('should throw ApiError on error response', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: () => Promise.resolve({ error: 'Dados inválidos' }),
      }),
    )

    const { apiRequest, ApiError } = await import('./api-client')

    await expect(apiRequest('/api/workouts')).rejects.toThrow(ApiError)
    await expect(apiRequest('/api/workouts')).rejects.toThrow('Dados inválidos')
  })
})
