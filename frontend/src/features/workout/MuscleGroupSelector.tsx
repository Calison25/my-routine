import type { MuscleGroup } from "../../types";

interface MuscleGroupSelectorProps {
  groups: MuscleGroup[];
  selectedIds: number[];
  onToggle: (id: number) => void;
  loading: boolean;
}

export default function MuscleGroupSelector({
  groups,
  selectedIds,
  onToggle,
  loading,
}: MuscleGroupSelectorProps) {
  if (loading) {
    return (
      <div className="flex flex-wrap gap-2">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="animate-pulse h-9 w-24 rounded-full bg-surface" />
        ))}
      </div>
    );
  }

  return (
    <div className="flex flex-wrap gap-2">
      {groups.map((group) => {
        const isSelected = selectedIds.includes(group.id);
        return (
          <button
            key={group.id}
            type="button"
            onClick={() => onToggle(group.id)}
            className={`rounded-full px-4 py-2 text-xs font-bold tracking-wide uppercase transition-all duration-300 ${
              isSelected
                ? "bg-primary text-on-primary shadow-[0_0_15px_rgba(0,206,209,0.3)]"
                : "bg-surface text-on-surface-variant hover:bg-surface-high"
            }`}
          >
            {group.name}
          </button>
        );
      })}
    </div>
  );
}
