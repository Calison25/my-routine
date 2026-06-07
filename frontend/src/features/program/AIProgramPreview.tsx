import { useState } from "react";
import { Dumbbell, Heart, Flower2, Loader2 } from "lucide-react";
import { createProgram } from "../../services";
import { useCategories } from "../../hooks/useCategories";
import type { CreateProgramInput } from "../../types";

const CATEGORY_ICONS: Record<number, React.ReactNode> = {
  1: <Dumbbell size={14} />,
  2: <Heart size={14} />,
  3: <Flower2 size={14} />,
};

interface AIProgramPreviewProps {
  program: CreateProgramInput;
  onSaved: () => void;
  onDiscard: () => void;
}

export default function AIProgramPreview({
  program,
  onSaved,
  onDiscard,
}: AIProgramPreviewProps) {
  const [saving, setSaving] = useState(false);
  const [feedback, setFeedback] = useState<{
    type: "success" | "error";
    message: string;
  } | null>(null);
  const { categories } = useCategories();

  const categoryNames = new Map(categories.map((c) => [c.id, c.name]));

  async function handleSave() {
    setSaving(true);
    setFeedback(null);

    try {
      await createProgram(program);
      setFeedback({ type: "success", message: "Programa criado com sucesso!" });
      setTimeout(onSaved, 800);
    } catch {
      setFeedback({
        type: "error",
        message: "Erro ao salvar programa. Tente novamente.",
      });
      setSaving(false);
    }
  }

  return (
    <div className="space-y-5">
      <div>
        <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
          Preview IA
        </span>
        <h3 className="text-lg font-extrabold tracking-tight text-on-bg">
          {program.name}
        </h3>
        <p className="text-xs text-outline mt-1">
          {program.slots.length} treino{program.slots.length !== 1 ? "s" : ""}
        </p>
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

      <div className="space-y-3">
        {program.slots.map((slot, index) => {
          const uniqueCategoryIds = Array.from(
            new Set(slot.categories.map((c) => c.category_id))
          );

          return (
            <div key={index} className="rounded-2xl bg-surface p-5">
              <div className="flex items-center gap-3 mb-3">
                <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary text-sm font-extrabold">
                  {slot.slot_label}
                </span>
                <span className="text-[10px] font-bold tracking-[0.1em] uppercase text-on-surface-variant">
                  Treino {slot.slot_label}
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {uniqueCategoryIds.map((catId) => (
                  <span
                    key={catId}
                    className="inline-flex items-center gap-1.5 rounded-full bg-primary-container/60 px-3 py-1.5 text-[11px] font-semibold text-primary"
                  >
                    {CATEGORY_ICONS[catId]}
                    {categoryNames.get(catId) ?? `Cat ${catId}`}
                  </span>
                ))}
              </div>
            </div>
          );
        })}
      </div>

      <div className="flex gap-3 pt-2">
        <button
          type="button"
          onClick={onDiscard}
          disabled={saving}
          className="flex-1 rounded-2xl border-2 border-outline-variant/40 py-4 text-xs font-bold tracking-wider uppercase text-outline hover:border-primary/50 hover:text-primary transition-all disabled:opacity-40"
        >
          Descartar
        </button>
        <button
          type="button"
          onClick={handleSave}
          disabled={saving}
          className="flex-1 rounded-2xl bg-primary py-4 text-sm font-extrabold uppercase tracking-wider text-on-primary transition-all hover:shadow-[0_0_25px_rgba(0,206,209,0.25)] disabled:opacity-40 disabled:cursor-not-allowed flex items-center justify-center gap-2"
        >
          {saving ? (
            <>
              <Loader2 size={16} className="animate-spin" />
              Salvando...
            </>
          ) : (
            "Salvar Programa"
          )}
        </button>
      </div>
    </div>
  );
}
