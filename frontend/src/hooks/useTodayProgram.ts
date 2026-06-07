import { useState, useEffect, useCallback } from "react";
import { getTodayProgram } from "../services";
import type { NextWorkoutOutput } from "../types";

export function useTodayProgram() {
  const [nextWorkout, setNextWorkout] = useState<NextWorkoutOutput | null>(
    null,
  );
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);
    getTodayProgram()
      .then(setNextWorkout)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { nextWorkout, loading, error, refresh };
}
