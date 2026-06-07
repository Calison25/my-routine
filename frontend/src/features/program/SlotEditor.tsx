import { Trash2, Dumbbell, Heart, Flower2 } from "lucide-react";
import type { TrainingCategory, MuscleGroup } from "../../types";

interface SlotEditorProps {
  label: string;
  selectedCategoryIds: number[];
  selectedMuscleGroupIds: number[];
  categories: TrainingCategory[];
  muscleGroups: MuscleGroup[];
  loadingMuscleGroups: boolean;
  onToggleCategory: (categoryId: number) => void;
  onToggleMuscleGroup: (groupId: number) => void;
  onRemove: () => void;
}

const CATEGORY_ICONS: Record<string, React.ReactNode> = {
  Musculação: <Dumbbell className="w-4 h-4" />,
  Cardio: <Heart className="w-4 h-4" />,
  Pilates: <Flower2 className="w-4 h-4" />,
};

const MUSCULACAO_ID = 1;

export default function SlotEditor({
  label,
  selectedCategoryIds,
  selectedMuscleGroupIds,
  categories,
  muscleGroups,
  loadingMuscleGroups,
  onToggleCategory,
  onToggleMuscleGroup,
  onRemove,
}: SlotEditorProps) {
  const hasMusculacao = selectedCategoryIds.includes(MUSCULACAO_ID);

  return (
    <div className="rounded-2xl bg-surface p-5">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-3">
          <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary text-sm font-extrabold">
            {label}
          </span>
          <span className="text-[10px] font-bold tracking-[0.1em] uppercase text-on-surface-variant">
            Treino {label}
          </span>
        </div>
        <button
          type="button"
          onClick={onRemove}
          className="flex items-center justify-center w-8 h-8 rounded-full text-outline hover:text-error hover:bg-error-dim/30 transition-all"
        >
          <Trash2 size={16} />
        </button>
      </div>

      <div className="space-y-4">
        <div>
          <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-3">
            Categorias
          </label>
          <div className="flex flex-wrap gap-2">
            {categories.map((category) => {
              const isSelected = selectedCategoryIds.includes(category.id);
              return (
                <button
                  key={category.id}
                  type="button"
                  onClick={() => onToggleCategory(category.id)}
                  className={`inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-bold tracking-wide uppercase transition-all duration-300 ${
                    isSelected
                      ? "bg-primary text-on-primary shadow-[0_0_15px_rgba(0,206,209,0.3)]"
                      : "bg-surface-high text-on-surface-variant hover:bg-surface-highest"
                  }`}
                >
                  {CATEGORY_ICONS[category.name] ?? <Dumbbell className="w-4 h-4" />}
                  {category.name}
                </button>
              );
            })}
          </div>
        </div>

        {hasMusculacao && (
          <div>
            <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-3">
              Grupos Musculares
            </label>
            {loadingMuscleGroups ? (
              <div className="flex flex-wrap gap-2">
                {[1, 2, 3, 4].map((i) => (
                  <div key={i} className="animate-pulse h-9 w-24 rounded-full bg-surface-high" />
                ))}
              </div>
            ) : (
              <div className="flex flex-wrap gap-2">
                {muscleGroups.map((group) => {
                  const isSelected = selectedMuscleGroupIds.includes(group.id);
                  return (
                    <button
                      key={group.id}
                      type="button"
                      onClick={() => onToggleMuscleGroup(group.id)}
                      className={`rounded-full px-4 py-2 text-xs font-bold tracking-wide uppercase transition-all duration-300 ${
                        isSelected
                          ? "bg-primary text-on-primary shadow-[0_0_15px_rgba(0,206,209,0.3)]"
                          : "bg-surface-high text-on-surface-variant hover:bg-surface-highest"
                      }`}
                    >
                      {group.name}
                    </button>
                  );
                })}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
