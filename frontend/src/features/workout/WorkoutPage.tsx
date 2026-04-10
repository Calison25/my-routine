import { useState } from "react";
import { useCategories } from "../../hooks/useCategories";
import { useMuscleGroups } from "../../hooks/useMuscleGroups";
import { useTodayWorkouts } from "../../hooks/useTodayWorkouts";
import { createWorkout } from "../../services";
import CategorySelector from "./CategorySelector";
import MuscleGroupSelector from "./MuscleGroupSelector";
import WorkoutForm from "./WorkoutForm";
import TodayDashboard from "./TodayDashboard";
import ErrorMessage from "../../components/ErrorMessage";

const MUSCULACAO_ID = 1;

export default function WorkoutPage() {
  const { categories, loading: loadingCategories, error: categoriesError } = useCategories();
  const { workouts: todayWorkouts, loading: loadingToday, refresh: refreshToday } = useTodayWorkouts();

  const [categoryId, setCategoryId] = useState<number | null>(null);
  const [muscleGroupIds, setMuscleGroupIds] = useState<number[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);

  const { groups, loading: loadingGroups } = useMuscleGroups(categoryId);

  const isMusculacao = categoryId === MUSCULACAO_ID;

  function handleSelectCategory(id: number) {
    setCategoryId(id);
    setMuscleGroupIds([]);
    setFeedback(null);
  }

  function handleToggleMuscleGroup(id: number) {
    setMuscleGroupIds((prev) =>
      prev.includes(id) ? prev.filter((gid) => gid !== id) : [...prev, id]
    );
  }

  function resetForm() {
    setCategoryId(null);
    setMuscleGroupIds([]);
  }

  async function handleSubmit(data: {
    date: string;
    done: boolean;
    duration_minutes?: number;
  }) {
    if (categoryId === null) return;

    setSubmitting(true);
    setFeedback(null);

    try {
      await createWorkout({
        date: data.date,
        category_id: categoryId,
        muscle_group_ids: isMusculacao && muscleGroupIds.length > 0
          ? muscleGroupIds
          : undefined,
        done: data.done,
        duration_minutes: data.duration_minutes,
      });
      setFeedback({ type: "success", message: "Treino registrado!" });
      resetForm();
      refreshToday();
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      const message = err instanceof Error ? err.message : "Erro ao salvar treino";
      setFeedback({ type: "error", message });
    } finally {
      setSubmitting(false);
    }
  }

  if (categoriesError) {
    return (
      <ErrorMessage
        message="Não foi possível carregar as categorias. Verifique se o servidor está rodando."
        onRetry={() => window.location.reload()}
      />
    );
  }

  const canShowForm = categoryId !== null && (!isMusculacao || muscleGroupIds.length > 0);

  return (
    <div className="px-5 py-6 max-w-lg mx-auto">
      <section className="mb-8">
        <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
          Resumo
        </span>
        <h2 className="text-2xl font-extrabold tracking-tight text-on-bg">
          Hoje
        </h2>
        <div className="mt-4">
          <TodayDashboard workouts={todayWorkouts} loading={loadingToday} />
        </div>
      </section>

      <div className="h-px bg-outline-variant/20 mb-8" />

      <section>
        <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
          Novo registro
        </span>
        <h2 className="text-2xl font-extrabold tracking-tight text-on-bg mb-6">
          Registrar Treino
        </h2>

        {feedback && (
          <div
            className={`mb-5 rounded-2xl px-5 py-3 text-sm font-semibold ${
              feedback.type === "success"
                ? "bg-success-dim/40 text-success"
                : "bg-error-dim/40 text-error"
            }`}
          >
            {feedback.message}
          </div>
        )}

        <div className="space-y-6">
          <div>
            <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-3">
              Categoria
            </label>
            <CategorySelector
              categories={categories}
              selectedId={categoryId}
              onSelect={handleSelectCategory}
              loading={loadingCategories}
            />
          </div>

          {isMusculacao && (
            <div>
              <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-3">
                Grupos musculares
              </label>
              <MuscleGroupSelector
                groups={groups}
                selectedIds={muscleGroupIds}
                onToggle={handleToggleMuscleGroup}
                loading={loadingGroups}
              />
            </div>
          )}

          {canShowForm && (
            <div className="pt-2">
              <WorkoutForm onSubmit={handleSubmit} submitting={submitting} />
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
