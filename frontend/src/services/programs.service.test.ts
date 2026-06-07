import { describe, it, expect, vi, beforeEach } from 'vitest'
import {
  createProgram,
  getActiveProgram,
  listPrograms,
  getTodayProgram,
  skipTodayWorkout,
} from './programs.service'

vi.mock('./api-client', () => ({
  apiRequest: vi.fn(),
}))

import { apiRequest } from './api-client'

const mockedApiRequest = vi.mocked(apiRequest)

describe('ProgramsService', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('should call correct endpoint for createProgram', async () => {
    const input = {
      name: 'Programa A',
      slots: [
        {
          slot_label: 'Treino A',
          categories: [{ category_id: 1, muscle_group_id: 1 }],
        },
      ],
    }
    const mockProgram = { id: '1', name: 'Programa A', is_active: true, created_at: '2026-01-01', slots: [] }
    mockedApiRequest.mockResolvedValue(mockProgram)

    const result = await createProgram(input)

    expect(apiRequest).toHaveBeenCalledWith('/api/programs/', {
      method: 'POST',
      body: JSON.stringify(input),
    })
    expect(result).toEqual(mockProgram)
  })

  it('should call correct endpoint for getActiveProgram', async () => {
    const mockProgram = { id: '1', name: 'Programa A', is_active: true, created_at: '2026-01-01', slots: [] }
    mockedApiRequest.mockResolvedValue(mockProgram)

    const result = await getActiveProgram()

    expect(apiRequest).toHaveBeenCalledWith('/api/programs/active')
    expect(result).toEqual(mockProgram)
  })

  it('should call correct endpoint for listPrograms', async () => {
    const mockPrograms = [{ id: '1', name: 'Programa A', is_active: true, created_at: '2026-01-01', slots: [] }]
    mockedApiRequest.mockResolvedValue(mockPrograms)

    const result = await listPrograms()

    expect(apiRequest).toHaveBeenCalledWith('/api/programs/')
    expect(result).toEqual(mockPrograms)
  })

  it('should call correct endpoint for getTodayProgram', async () => {
    const mockNext = {
      slot_label: 'Treino A',
      slot_order: 1,
      program_name: 'Programa A',
      categories: [{ category_id: 1, muscle_group_id: null }],
    }
    mockedApiRequest.mockResolvedValue(mockNext)

    const result = await getTodayProgram()

    expect(apiRequest).toHaveBeenCalledWith('/api/workouts/today-program')
    expect(result).toEqual(mockNext)
  })

  it('should call correct endpoint for skipTodayWorkout', async () => {
    mockedApiRequest.mockResolvedValue(undefined)

    await skipTodayWorkout()

    expect(apiRequest).toHaveBeenCalledWith('/api/workouts/skip-today', {
      method: 'POST',
    })
  })
})
