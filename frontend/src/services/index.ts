export { apiRequest, ApiError } from './api-client'
export { getCategories, getMuscleGroups } from './categories.service'
export { createWorkout, getWorkoutsByDate, getCalendar } from './workouts.service'
export {
  createProgram,
  getActiveProgram,
  listPrograms,
  getTodayProgram,
  skipTodayWorkout,
} from './programs.service'
export { transcribeAudio, generateProgram } from './ai.service'
