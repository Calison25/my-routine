import { useState, useCallback } from "react";
import { Dumbbell, Heart, Flower2, Plus, Mic, PenLine } from "lucide-react";
import { useActiveProgram } from "../../hooks/usePrograms";
import { useCategories } from "../../hooks/useCategories";
import ProgramBuilder from "./ProgramBuilder";
import AudioRecorder from "./AudioRecorder";
import AIProgramPreview from "./AIProgramPreview";
import ErrorMessage from "../../components/ErrorMessage";
import type { WorkoutSlot, CreateProgramInput } from "../../types";

type CreationMode = "manual" | "voice";

const CATEGORY_ICONS: Record<number, React.ReactNode> = {
  1: <Dumbbell size={14} />,
  2: <Heart size={14} />,
  3: <Flower2 size={14} />,
};

function SlotCard({
  slot,
  categoryNames,
}: {
  slot: WorkoutSlot;
  categoryNames: Map<number, string>;
}) {
  return (
    <div className="rounded-2xl bg-surface p-5">
      <div className="flex items-center gap-3 mb-3">
        <span className="flex items-center justify-center w-8 h-8 rounded-full bg-primary/20 text-primary text-sm font-extrabold">
          {slot.slot_label}
        </span>
        <span className="text-[10px] font-bold tracking-[0.1em] uppercase text-on-surface-variant">
          Treino {slot.slot_label}
        </span>
      </div>
      <div className="flex flex-wrap gap-2">
        {Array.from(new Set(slot.categories.map((c) => c.category_id))).map(
          (catId) => (
            <span
              key={catId}
              className="inline-flex items-center gap-1.5 rounded-full bg-primary-container/60 px-3 py-1.5 text-[11px] font-semibold text-primary"
            >
              {CATEGORY_ICONS[catId]}
              {categoryNames.get(catId) ?? `Cat ${catId}`}
            </span>
          )
        )}
      </div>
    </div>
  );
}

function CreationModeTabs({
  mode,
  onChange,
}: {
  mode: CreationMode;
  onChange: (m: CreationMode) => void;
}) {
  return (
    <div className="flex rounded-2xl bg-surface p-1 gap-1">
      <button
        type="button"
        onClick={() => onChange("manual")}
        className={`flex-1 flex items-center justify-center gap-2 rounded-xl py-3 text-xs font-bold tracking-wider uppercase transition-all ${
          mode === "manual"
            ? "bg-primary text-on-primary"
            : "text-outline hover:text-on-surface"
        }`}
      >
        <PenLine size={14} />
        Manual
      </button>
      <button
        type="button"
        onClick={() => onChange("voice")}
        className={`flex-1 flex items-center justify-center gap-2 rounded-xl py-3 text-xs font-bold tracking-wider uppercase transition-all ${
          mode === "voice"
            ? "bg-primary text-on-primary"
            : "text-outline hover:text-on-surface"
        }`}
      >
        <Mic size={14} />
        Por Voz
      </button>
    </div>
  );
}

export default function ProgramPage() {
  const { program, loading, error, refresh } = useActiveProgram();
  const { categories } = useCategories();
  const [showBuilder, setShowBuilder] = useState(false);
  const [creationMode, setCreationMode] = useState<CreationMode>("manual");
  const [generatedProgram, setGeneratedProgram] =
    useState<CreateProgramInput | null>(null);
  const [aiError, setAiError] = useState<string | null>(null);

  const categoryNames = new Map(categories.map((c) => [c.id, c.name]));

  const handleProgramGenerated = useCallback(
    (prog: CreateProgramInput) => {
      setGeneratedProgram(prog);
      setAiError(null);
    },
    []
  );

  const handleAiError = useCallback((message: string) => {
    setAiError(message);
  }, []);

  function handleCreated() {
    setShowBuilder(false);
    setGeneratedProgram(null);
    setCreationMode("manual");
    refresh();
  }

  function handleCancelBuilder() {
    setShowBuilder(false);
    setGeneratedProgram(null);
    setAiError(null);
    setCreationMode("manual");
  }

  if (error) {
    return (
      <ErrorMessage
        message="Não foi possível carregar o programa. Verifique se o servidor está rodando."
        onRetry={refresh}
      />
    );
  }

  if (showBuilder) {
    return (
      <div className="px-5 py-6 max-w-lg mx-auto">
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
              onClick={handleCancelBuilder}
              className="text-xs font-bold tracking-wider uppercase text-outline hover:text-on-surface transition-colors"
            >
              Cancelar
            </button>
          </div>

          <CreationModeTabs mode={creationMode} onChange={setCreationMode} />

          {aiError && (
            <div className="rounded-2xl px-5 py-3 text-sm font-semibold bg-error-dim/40 text-error">
              {aiError}
            </div>
          )}

          {creationMode === "manual" && (
            <ProgramBuilder
              onCreated={handleCreated}
              onCancel={handleCancelBuilder}
            />
          )}

          {creationMode === "voice" && !generatedProgram && (
            <AudioRecorder
              onProgramGenerated={handleProgramGenerated}
              onError={handleAiError}
            />
          )}

          {creationMode === "voice" && generatedProgram && (
            <AIProgramPreview
              program={generatedProgram}
              onSaved={handleCreated}
              onDiscard={() => {
                setGeneratedProgram(null);
                setAiError(null);
              }}
            />
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="px-5 py-6 max-w-lg mx-auto">
      <section>
        <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
          Planejamento
        </span>
        <h2 className="text-2xl font-extrabold tracking-tight text-on-bg">
          Programa
        </h2>
      </section>

      <div className="mt-6">
        {loading ? (
          <div className="space-y-3">
            <div className="animate-pulse rounded-2xl bg-surface h-24" />
            <div className="animate-pulse rounded-2xl bg-surface h-24" />
          </div>
        ) : program ? (
          <div className="space-y-6">
            <div className="rounded-2xl bg-surface-high p-5">
              <span className="text-[10px] font-bold tracking-[0.1em] uppercase text-on-surface-variant block mb-1">
                Programa ativo
              </span>
              <h3 className="text-lg font-extrabold text-on-surface">
                {program.name}
              </h3>
              <p className="text-xs text-outline mt-1">
                {program.slots.length} treino
                {program.slots.length !== 1 ? "s" : ""}
              </p>
            </div>

            <div className="space-y-3">
              {program.slots
                .sort((a, b) => a.slot_order - b.slot_order)
                .map((slot) => (
                  <SlotCard
                    key={slot.id}
                    slot={slot}
                    categoryNames={categoryNames}
                  />
                ))}
            </div>

            <button
              type="button"
              onClick={() => setShowBuilder(true)}
              className="flex items-center gap-2 w-full justify-center rounded-2xl border-2 border-dashed border-outline-variant/40 py-4 text-xs font-bold tracking-wider uppercase text-outline hover:border-primary/50 hover:text-primary transition-all"
            >
              <Plus size={16} />
              Criar Novo Programa
            </button>
          </div>
        ) : (
          <div className="text-center py-12">
            <div className="mx-auto w-16 h-16 rounded-full bg-surface flex items-center justify-center mb-4">
              <Dumbbell className="w-8 h-8 text-outline" />
            </div>
            <p className="text-sm text-outline font-light mb-6">
              Nenhum programa ativo
            </p>
            <button
              type="button"
              onClick={() => setShowBuilder(true)}
              className="rounded-2xl bg-primary px-8 py-4 text-sm font-extrabold uppercase tracking-wider text-on-primary transition-all hover:shadow-[0_0_25px_rgba(0,206,209,0.25)]"
            >
              Criar Programa
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
