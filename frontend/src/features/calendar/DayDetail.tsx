import { useState, useEffect } from "react";
import { X, Dumbbell, Heart, Flower2, Clock } from "lucide-react";
import { getWorkoutsByDate } from "../../services";
import type { WorkoutDetail } from "../../types";

interface DayDetailProps {
  date: string;
  onClose: () => void;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  Musculação: <Dumbbell size={16} />,
  Cardio: <Heart size={16} />,
  Pilates: <Flower2 size={16} />,
};

function formatDate(iso: string): string {
  const [y, m, d] = iso.split("-");
  return `${d}/${m}/${y}`;
}

export default function DayDetail({ date, onClose }: DayDetailProps) {
  const [workouts, setWorkouts] = useState<WorkoutDetail[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    getWorkoutsByDate(date)
      .then(setWorkouts)
      .catch(() => setWorkouts([]))
      .finally(() => setLoading(false));
  }, [date]);

  return (
    <div className="mt-6 rounded-2xl bg-surface overflow-hidden">
      <div className="flex items-center justify-between px-5 py-4">
        <div>
          <span className="text-[10px] tracking-[0.1em] uppercase font-bold text-primary/70 block">
            Detalhe
          </span>
          <h3 className="text-sm font-bold text-on-surface">
            {formatDate(date)}
          </h3>
        </div>
        <button
          type="button"
          onClick={onClose}
          className="p-1.5 rounded-full text-outline hover:text-on-surface hover:bg-surface-high transition-colors"
        >
          <X size={16} />
        </button>
      </div>

      <div className="px-5 pb-5">
        {loading ? (
          <div className="space-y-2">
            <div className="animate-pulse h-12 rounded-xl bg-surface-high" />
            <div className="animate-pulse h-12 rounded-xl bg-surface-high" />
          </div>
        ) : workouts.length === 0 ? (
          <p className="text-sm text-outline text-center py-4 font-light">
            Nenhum treino neste dia
          </p>
        ) : (
          <div className="space-y-2">
            {workouts.map((w) => (
              <div
                key={w.id}
                className={`flex items-center gap-3 rounded-xl px-4 py-3 text-sm ${
                  w.done
                    ? "bg-primary/10"
                    : "bg-surface-high"
                }`}
              >
                <span className={w.done ? "text-primary" : "text-outline"}>
                  {CATEGORY_ICONS[w.category_name] ?? <Dumbbell size={16} />}
                </span>
                <div className="flex-1 min-w-0">
                  <span className={`font-semibold ${w.done ? "text-on-surface" : "text-outline"}`}>
                    {w.category_name}
                  </span>
                  {w.muscle_group_name && (
                    <span className="text-on-surface-variant"> — {w.muscle_group_name}</span>
                  )}
                </div>
                {w.duration_minutes && (
                  <span className="flex items-center gap-1 text-xs text-on-surface-variant">
                    <Clock size={12} />
                    {w.duration_minutes}min
                  </span>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
