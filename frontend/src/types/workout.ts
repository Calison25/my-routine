export interface CreateWorkoutDTO {
  date: string
  category_id: number
  muscle_group_ids?: number[]
  done: boolean
  duration_minutes?: number
}

export interface WorkoutDetail {
  id: string
  date: string
  category_id: number
  category_name: string
  muscle_group_id: number | null
  muscle_group_name: string | null
  done: boolean
  duration_minutes: number | null
}

export interface CalendarDay {
  date: string
  done: boolean
  count: number
}

export interface WorkoutCalendar {
  days: CalendarDay[]
}
