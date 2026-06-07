import { apiRequest } from './api-client'
import type { WorkoutProgram, CreateProgramInput, NextWorkoutOutput } from '../types'

export async function createProgram(data: CreateProgramInput): Promise<WorkoutProgram> {
  return apiRequest<WorkoutProgram>('/api/programs/', {
    method: 'POST',
    body: JSON.stringify(data),
  })
}

export async function getActiveProgram(): Promise<WorkoutProgram | null> {
  return apiRequest<WorkoutProgram | null>('/api/programs/active')
}

export async function listPrograms(): Promise<WorkoutProgram[]> {
  return apiRequest<WorkoutProgram[]>('/api/programs/')
}

export async function getTodayProgram(): Promise<NextWorkoutOutput | null> {
  return apiRequest<NextWorkoutOutput | null>('/api/workouts/today-program')
}

export async function skipTodayWorkout(): Promise<void> {
  await apiRequest<void>('/api/workouts/skip-today', {
    method: 'POST',
  })
}
