import { useState, useEffect, useCallback } from "react";
import { getActiveProgram, createProgram } from "../services";
import type { WorkoutProgram, CreateProgramInput } from "../types";

export function useActiveProgram() {
  const [program, setProgram] = useState<WorkoutProgram | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const refresh = useCallback(() => {
    setLoading(true);
    setError(null);
    getActiveProgram()
      .then(setProgram)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  return { program, loading, error, refresh };
}

export function useCreateProgram() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const create = useCallback(async (input: CreateProgramInput): Promise<WorkoutProgram> => {
    setLoading(true);
    setError(null);
    try {
      const result = await createProgram(input);
      return result;
    } catch (e) {
      const message = e instanceof Error ? e.message : "Erro ao criar programa";
      setError(message);
      throw e;
    } finally {
      setLoading(false);
    }
  }, []);

  return { create, loading, error };
}
