import { useState } from "react";
import { Link } from "react-router-dom";
import { CalendarCheck, SkipForward, Dumbbell, Heart, Flower2 } from "lucide-react";
import { skipTodayWorkout, createWorkout } from "../../services";
import { useCategories } from "../../hooks/useCategories";
import type { NextWorkoutOutput, SlotCategory } from "../../types";

interface TodayProgramWidgetProps {
  nextWorkout: NextWorkoutOutput | null;
  loading: boolean;
  onRefresh: () => void;
  onWorkoutRegistered: () => void;
}

const CATEGORY_ICONS: Record<number, React.ReactNode> = {
  1: <Dumbbell className="w-4 h-4" />,
  2: <Heart className="w-4 h-4" />,
  3: <Flower2 className="w-4 h-4" />,
};

function SkeletonWidget() {
  return (
    <div className="animate-pulse rounded-2xl bg-surface p-5">
      <div className="h-4 w-32 rounded bg-surface-high mb-4" />
      <div className="h-3 w-48 rounded bg-surface-high mb-3" />
      <div className="flex gap-2 mb-4">
        <div className="h-8 w-24 rounded-xl bg-surface-high" />
        <div className="h-8 w-24 rounded-xl bg-surface-high" />
      </div>
      <div className="flex gap-3">
        <div className="h-10 flex-1 rounded-full bg-surface-high" />
        <div className="h-10 w-24 rounded-full bg-surface-high" />
      </div>
    </div>
  );
}

function CategoryChip({
  slotCategory,
  categoryName,
}: {
  slotCategory: SlotCategory;
  categoryName: string;
}) {
  return (
    <span className="inline-flex items-center gap-1.5 rounded-xl bg-surface-high px-3 py-1.5 text-[11px] font-bold uppercase tracking-wide text-on-surface-variant">
      {CATEGORY_ICONS[slotCategory.category_id] ?? (
        <Dumbbell className="w-4 h-4" />
      )}
      {categoryName}
    </span>
  );
}

function todayISO(): string {
  return new Date().toISOString().split("T")[0];
}

export default function TodayProgramWidget({
  nextWorkout,
  loading,
  onRefresh,
  onWorkoutRegistered,
}: TodayProgramWidgetProps) {
  const { categories } = useCategories();
  const [submitting, setSubmitting] = useState(false);
  const [skipping, setSkipping] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);

  function getCategoryName(categoryId: number): string {
    return categories.find((c) => c.id === categoryId)?.name ?? `Categoria ${categoryId}`;
  }

  async function handleComplete() {
    if (!nextWorkout) return;
    setSubmitting(true);
    setFeedback(null);

    try {
      for (let i = 0; i < nextWorkout.categories.length; i++) {
        const slotCat = nextWorkout.categories[i];
        await createWorkout({
          date: todayISO(),
          category_id: slotCat.category_id,
          muscle_group_ids: slotCat.muscle_group_id
            ? [slotCat.muscle_group_id]
            : undefined,
          done: true,
          program_slot_id: i === 0 ? nextWorkout.slot_id : undefined,
        });
      }
      setFeedback({ type: "success", message: "Treino concluído!" });
      onRefresh();
      onWorkoutRegistered();
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Erro ao registrar treino";
      setFeedback({ type: "error", message });
    } finally {
      setSubmitting(false);
    }
  }

  async function handleSkip() {
    setSkipping(true);
    setFeedback(null);

    try {
      await skipTodayWorkout();
      setFeedback({ type: "success", message: "Treino pulado." });
      onRefresh();
      setTimeout(() => setFeedback(null), 3000);
    } catch (err) {
      const message =
        err instanceof Error ? err.message : "Erro ao pular treino";
      setFeedback({ type: "error", message });
    } finally {
      setSkipping(false);
    }
  }

  if (loading) {
    return <SkeletonWidget />;
  }

  if (!nextWorkout) {
    return (
      <div className="rounded-2xl bg-surface p-5 text-center">
        <p className="text-sm text-on-surface-variant mb-3">
          Nenhum programa ativo
        </p>
        <Link
          to="/programa"
          className="inline-block rounded-full bg-primary/10 px-5 py-2 text-xs font-bold uppercase tracking-widest text-primary transition-colors hover:bg-primary/20"
        >
          Criar programa
        </Link>
      </div>
    );
  }

  return (
    <div className="rounded-2xl bg-surface p-5">
      <div className="flex items-center justify-between mb-1">
        <h3 className="text-base font-extrabold text-on-surface">
          {nextWorkout.program_name}
        </h3>
      </div>

      <p className="text-xs font-bold uppercase tracking-wide text-primary/70 mb-4">
        {nextWorkout.slot_label}
      </p>

      <div className="flex flex-wrap gap-2 mb-5">
        {nextWorkout.categories.map((slotCat, index) => (
          <CategoryChip
            key={index}
            slotCategory={slotCat}
            categoryName={getCategoryName(slotCat.category_id)}
          />
        ))}
      </div>

      {feedback && (
        <div
          className={`mb-4 rounded-2xl px-4 py-2.5 text-xs font-semibold ${
            feedback.type === "success"
              ? "bg-success-dim/40 text-success"
              : "bg-error-dim/40 text-error"
          }`}
        >
          {feedback.message}
        </div>
      )}

      <div className="flex gap-3">
        <button
          type="button"
          disabled={submitting || skipping}
          onClick={handleComplete}
          className={`flex-1 flex items-center justify-center gap-2 h-11 rounded-full font-bold tracking-[0.1em] uppercase text-xs transition-all duration-300 ${
            submitting
              ? "bg-primary/50 text-on-primary cursor-wait"
              : "bg-primary text-on-primary hover:bg-primary/90 shadow-[0_0_20px_rgba(0,206,209,0.2)]"
          }`}
        >
          <CalendarCheck size={16} />
          {submitting ? "Salvando..." : "Concluir"}
        </button>

        <button
          type="button"
          disabled={submitting || skipping}
          onClick={handleSkip}
          className={`flex items-center justify-center gap-2 px-5 h-11 rounded-full font-bold tracking-[0.1em] uppercase text-xs transition-all duration-300 ${
            skipping
              ? "bg-surface-high text-outline cursor-wait"
              : "bg-surface-high text-on-surface-variant hover:bg-outline-variant/30"
          }`}
        >
          <SkipForward size={14} />
          {skipping ? "..." : "Pular"}
        </button>
      </div>
    </div>
  );
}
