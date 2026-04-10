import { apiRequest } from './api-client'
import type { CreateWorkoutDTO, WorkoutDetail, WorkoutCalendar } from '../types'

export async function createWorkout(data: CreateWorkoutDTO): Promise<{ ids: string[] }> {
  return apiRequest<{ ids: string[] }>('/api/workouts', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function getWorkoutsByDate(date: string): Promise<WorkoutDetail[]> {
  return apiRequest<WorkoutDetail[]>(`/api/workouts?target_date=${date}`)
}

export async function getCalendar(month: number, year: number): Promise<WorkoutCalendar> {
  return apiRequest<WorkoutCalendar>(`/api/workouts/calendar?month=${month}&year=${year}`)
}
