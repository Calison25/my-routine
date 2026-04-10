import { useState, useEffect } from "react";
import { getCategories } from "../services";
import type { TrainingCategory } from "../types";

export function useCategories() {
  const [categories, setCategories] = useState<TrainingCategory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getCategories()
      .then(setCategories)
      .catch((e: Error) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  return { categories, loading, error };
}
