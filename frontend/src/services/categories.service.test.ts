import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getCategories, getMuscleGroups } from './categories.service'

vi.mock('./api-client', () => ({
  apiRequest: vi.fn(),
}))

import { apiRequest } from './api-client'

const mockedApiRequest = vi.mocked(apiRequest)

describe('CategoriesService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should call correct endpoint for getCategories', async () => {
    const mockCategories = [{ id: 1, name: 'Musculação' }]
    mockedApiRequest.mockResolvedValue(mockCategories)

    const result = await getCategories()

    expect(apiRequest).toHaveBeenCalledWith('/api/categories')
    expect(result).toEqual(mockCategories)
  })

  it('should call correct endpoint for getMuscleGroups', async () => {
    const mockGroups = [{ id: 1, name: 'Peito', category_id: 1 }]
    mockedApiRequest.mockResolvedValue(mockGroups)

    const result = await getMuscleGroups(1)

    expect(apiRequest).toHaveBeenCalledWith('/api/categories/1/muscle-groups')
    expect(result).toEqual(mockGroups)
  })
})
