import { useState, useEffect } from "react";
import { Plus } from "lucide-react";
import { useCategories } from "../../hooks/useCategories";
import { getMuscleGroups } from "../../services";
import { useCreateProgram } from "../../hooks/usePrograms";
import SlotEditor from "./SlotEditor";
import type { MuscleGroup, CreateSlotInput, CreateSlotCategoryInput } from "../../types";

interface SlotState {
  categoryIds: number[];
  muscleGroupIds: number[];
}

interface ProgramBuilderProps {
  onCreated: () => void;
  onCancel: () => void;
}

const MUSCULACAO_ID = 1;

function slotLabel(index: number): string {
  return String.fromCharCode(65 + index);
}

export default function ProgramBuilder({ onCreated, onCancel }: ProgramBuilderProps) {
  const [name, setName] = useState("");
  const [slots, setSlots] = useState<SlotState[]>([{ categoryIds: [], muscleGroupIds: [] }]);
  const [muscleGroups, setMuscleGroups] = useState<MuscleGroup[]>([]);
  const [loadingMuscleGroups, setLoadingMuscleGroups] = useState(false);
  const [feedback, setFeedback] = useState<{ type: "success" | "error"; message: string } | null>(null);

  const { categories, loading: loadingCategories } = useCategories();
  const { create, loading: submitting } = useCreateProgram();

  const anySlotHasMusculacao = slots.some((s) => s.categoryIds.includes(MUSCULACAO_ID));

  useEffect(() => {
    if (!anySlotHasMusculacao) {
      setMuscleGroups([]);
      return;
    }
    if (muscleGroups.length > 0) return;

    setLoadingMuscleGroups(true);
    getMuscleGroups(MUSCULACAO_ID)
      .then(setMuscleGroups)
      .finally(() => setLoadingMuscleGroups(false));
  }, [anySlotHasMusculacao, muscleGroups.length]);

  function updateSlot(index: number, partial: Partial<SlotState>) {
    setSlots((prev) => prev.map((s, i) => (i === index ? { ...s, ...partial } : s)));
  }

  function handleToggleCategory(slotIndex: number, categoryId: number) {
    const slot = slots[slotIndex];
    const newIds = slot.categoryIds.includes(categoryId)
      ? slot.categoryIds.filter((id) => id !== categoryId)
      : [...slot.categoryIds, categoryId];

    const removedMusculacao = categoryId === MUSCULACAO_ID && !newIds.includes(MUSCULACAO_ID);
    updateSlot(slotIndex, {
      categoryIds: newIds,
      muscleGroupIds: removedMusculacao ? [] : slot.muscleGroupIds,
    });
  }

  function handleToggleMuscleGroup(slotIndex: number, groupId: number) {
    const slot = slots[slotIndex];
    const newIds = slot.muscleGroupIds.includes(groupId)
      ? slot.muscleGroupIds.filter((id) => id !== groupId)
      : [...slot.muscleGroupIds, groupId];
    updateSlot(slotIndex, { muscleGroupIds: newIds });
  }

  function addSlot() {
    setSlots((prev) => [...prev, { categoryIds: [], muscleGroupIds: [] }]);
  }

  function removeSlot(index: number) {
    setSlots((prev) => prev.filter((_, i) => i !== index));
  }

  function buildSlotInputs(): CreateSlotInput[] {
    return slots.map((slot, index) => {
      const slotCategories: CreateSlotCategoryInput[] = [];

      for (const catId of slot.categoryIds) {
        if (catId === MUSCULACAO_ID && slot.muscleGroupIds.length > 0) {
          for (const mgId of slot.muscleGroupIds) {
            slotCategories.push({ category_id: catId, muscle_group_id: mgId });
          }
        } else {
          slotCategories.push({ category_id: catId });
        }
      }

      return {
        slot_label: slotLabel(index),
        categories: slotCategories,
      };
    });
  }

  function isValid(): boolean {
    if (!name.trim()) return false;
    if (slots.length === 0) return false;
    return slots.every((s) => s.categoryIds.length > 0);
  }

  async function handleSubmit() {
    if (!isValid()) return;

    setFeedback(null);
    try {
      await create({ name: name.trim(), slots: buildSlotInputs() });
      setFeedback({ type: "success", message: "Programa criado!" });
      setTimeout(onCreated, 800);
    } catch {
      setFeedback({ type: "error", message: "Erro ao criar programa. Tente novamente." });
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
            Novo
          </span>
          <h2 className="text-2xl font-extrabold tracking-tight text-on-bg">
            Criar Programa
          </h2>
        </div>
        <button
          type="button"
          onClick={onCancel}
          className="text-xs font-bold tracking-wider uppercase text-outline hover:text-on-surface transition-colors"
        >
          Cancelar
        </button>
      </div>

      {feedback && (
        <div
          className={`rounded-2xl px-5 py-3 text-sm font-semibold ${
            feedback.type === "success"
              ? "bg-success-dim/40 text-success"
              : "bg-error-dim/40 text-error"
          }`}
        >
          {feedback.message}
        </div>
      )}

      <div>
        <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
          Nome do programa
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Ex: Meu Programa ABC"
          className="w-full rounded-2xl bg-surface px-5 py-3.5 text-sm text-on-surface placeholder:text-outline focus:outline-none focus:ring-2 focus:ring-primary/40 transition-all"
        />
      </div>

      {loadingCategories ? (
        <div className="animate-pulse rounded-2xl bg-surface h-32" />
      ) : (
        <div className="space-y-4">
          {slots.map((slot, index) => (
            <SlotEditor
              key={index}
              label={slotLabel(index)}
              selectedCategoryIds={slot.categoryIds}
              selectedMuscleGroupIds={slot.muscleGroupIds}
              categories={categories}
              muscleGroups={muscleGroups}
              loadingMuscleGroups={loadingMuscleGroups}
              onToggleCategory={(catId) => handleToggleCategory(index, catId)}
              onToggleMuscleGroup={(mgId) => handleToggleMuscleGroup(index, mgId)}
              onRemove={() => removeSlot(index)}
            />
          ))}
        </div>
      )}

      <button
        type="button"
        onClick={addSlot}
        className="flex items-center gap-2 w-full justify-center rounded-2xl border-2 border-dashed border-outline-variant/40 py-4 text-xs font-bold tracking-wider uppercase text-outline hover:border-primary/50 hover:text-primary transition-all"
      >
        <Plus size={16} />
        Adicionar Treino
      </button>

      <button
        type="button"
        onClick={handleSubmit}
        disabled={!isValid() || submitting}
        className="w-full rounded-2xl bg-primary py-4 text-sm font-extrabold uppercase tracking-wider text-on-primary transition-all hover:shadow-[0_0_25px_rgba(0,206,209,0.25)] disabled:opacity-40 disabled:cursor-not-allowed"
      >
        {submitting ? "Salvando..." : "Salvar Programa"}
      </button>
    </div>
  );
}
