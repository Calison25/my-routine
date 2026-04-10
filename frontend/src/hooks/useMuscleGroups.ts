import { useState, useEffect } from "react";
import { getMuscleGroups } from "../services";
import type { MuscleGroup } from "../types";

const MUSCULACAO_ID = 1;

export function useMuscleGroups(categoryId: number | null) {
  const [groups, setGroups] = useState<MuscleGroup[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (categoryId === null || categoryId !== MUSCULACAO_ID) {
      setGroups([]);
      return;
    }
    setLoading(true);
    getMuscleGroups(categoryId)
      .then(setGroups)
      .finally(() => setLoading(false));
  }, [categoryId]);

  return { groups, loading };
}
