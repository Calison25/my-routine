import { useState, useEffect } from 'react'
import { getCalendar } from '../services'
import type { WorkoutCalendar } from '../types'

export function useWorkoutCalendar(month: number, year: number) {
  const [calendar, setCalendar] = useState<WorkoutCalendar | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    setLoading(true)
    setError(null)
    getCalendar(month, year)
      .then(setCalendar)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false))
  }, [month, year])

  return { calendar, loading, error }
}
