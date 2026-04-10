import { Dumbbell, Heart, Flower2 } from "lucide-react";
import type { TrainingCategory } from "../../types";

interface CategorySelectorProps {
  categories: TrainingCategory[];
  selectedId: number | null;
  onSelect: (id: number) => void;
  loading: boolean;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  Musculação: <Dumbbell className="w-6 h-6" />,
  Cardio: <Heart className="w-6 h-6" />,
  Pilates: <Flower2 className="w-6 h-6" />,
};

function SkeletonCard() {
  return (
    <div className="animate-pulse rounded-2xl bg-surface p-6">
      <div className="mx-auto mb-3 h-10 w-10 rounded-full bg-surface-high" />
      <div className="mx-auto h-3 w-16 rounded bg-surface-high" />
    </div>
  );
}

export default function CategorySelector({
  categories,
  selectedId,
  onSelect,
  loading,
}: CategorySelectorProps) {
  if (loading) {
    return (
      <div className="grid grid-cols-3 gap-3">
        <SkeletonCard />
        <SkeletonCard />
        <SkeletonCard />
      </div>
    );
  }

  return (
    <div className="grid grid-cols-3 gap-3">
      {categories.map((category) => {
        const isSelected = category.id === selectedId;
        return (
          <button
            key={category.id}
            type="button"
            onClick={() => onSelect(category.id)}
            className={`flex flex-col items-center gap-3 rounded-2xl p-5 transition-all duration-300 ${
              isSelected
                ? "bg-primary-container text-primary shadow-[0_0_20px_rgba(0,206,209,0.15)]"
                : "bg-surface text-on-surface-variant hover:bg-surface-high"
            }`}
          >
            <div
              className={`w-10 h-10 rounded-full flex items-center justify-center transition-colors ${
                isSelected ? "bg-primary/20" : "bg-surface-high"
              }`}
            >
              {CATEGORY_ICONS[category.name] ?? <Dumbbell className="w-6 h-6" />}
            </div>
            <span className="text-[10px] font-bold tracking-[0.05em] uppercase">
              {category.name}
            </span>
          </button>
        );
      })}
    </div>
  );
}
