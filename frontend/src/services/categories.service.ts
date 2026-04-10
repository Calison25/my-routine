import { apiRequest } from './api-client'
import type { TrainingCategory, MuscleGroup } from '../types'

export async function getCategories(): Promise<TrainingCategory[]> {
  return apiRequest<TrainingCategory[]>('/api/categories')
}

export async function getMuscleGroups(categoryId: number): Promise<MuscleGroup[]> {
  return apiRequest<MuscleGroup[]>(`/api/categories/${categoryId}/muscle-groups`)
}
