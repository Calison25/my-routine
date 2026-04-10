import { useState, useEffect, useCallback } from "react";
import { getWorkoutsByDate } from "../services";
import type { WorkoutDetail } from "../types";

function todayISO(): string {
  return new Date().toISOString().split("T")[0];
}

export function useTodayWorkouts() {
  const [workouts, setWorkouts] = useState<WorkoutDetail[]>([]);
  const [loading, setLoading] = useState(true);

  const refresh = useCallback(() => {
    setLoading(true);
    getWorkoutsByDate(todayISO())
      .then(setWorkouts)
      .catch(() => setWorkouts([]))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { workouts, loading, refresh };
}
