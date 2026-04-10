import { Dumbbell, Heart, Flower2, Clock } from "lucide-react";
import type { WorkoutDetail } from "../../types";

interface TodayDashboardProps {
  workouts: WorkoutDetail[];
  loading: boolean;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  Musculação: <Dumbbell size={16} />,
  Cardio: <Heart size={16} />,
  Pilates: <Flower2 size={16} />,
};

export default function TodayDashboard({ workouts, loading }: TodayDashboardProps) {
  if (loading) {
    return (
      <div className="animate-pulse rounded-2xl bg-surface h-20" />
    );
  }

  const doneWorkouts = workouts.filter((w) => w.done);

  if (doneWorkouts.length === 0) {
    return (
      <div className="rounded-2xl bg-surface p-5 text-center">
        <p className="text-sm text-outline font-light">
          Nenhum treino registrado hoje
        </p>
      </div>
    );
  }

  const grouped = new Map<string, WorkoutDetail[]>();
  for (const w of doneWorkouts) {
    const key = w.category_name;
    if (!grouped.has(key)) grouped.set(key, []);
    grouped.get(key)!.push(w);
  }

  return (
    <div className="space-y-3">
      {Array.from(grouped.entries()).map(([category, items]) => (
        <div
          key={category}
          className="rounded-2xl bg-surface p-5"
        >
          <div className="flex items-center gap-2 mb-3">
            <span className="text-primary">
              {CATEGORY_ICONS[category] ?? <Dumbbell size={16} />}
            </span>
            <span className="text-[10px] font-bold tracking-[0.1em] uppercase text-on-surface">
              {category}
            </span>
          </div>
          <div className="flex flex-wrap gap-2">
            {items.map((w) => (
              <span
                key={w.id}
                className="inline-flex items-center gap-1.5 rounded-full bg-success-dim/50 px-3 py-1.5 text-[11px] font-semibold text-success"
              >
                {w.muscle_group_name ?? "Feito"}
                {w.duration_minutes && (
                  <span className="inline-flex items-center gap-0.5 text-success/70">
                    <Clock size={10} />
                    {w.duration_minutes}min
                  </span>
                )}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
