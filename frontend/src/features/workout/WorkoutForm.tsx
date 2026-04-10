import { useState } from "react";
import { Check, X } from "lucide-react";

interface WorkoutFormData {
  date: string;
  done: boolean;
  duration_minutes?: number;
}

interface WorkoutFormProps {
  onSubmit: (data: WorkoutFormData) => void;
  submitting: boolean;
}

function todayISO(): string {
  return new Date().toISOString().split("T")[0];
}

export default function WorkoutForm({ onSubmit, submitting }: WorkoutFormProps) {
  const [date, setDate] = useState(todayISO());
  const [done, setDone] = useState<boolean | null>(null);
  const [duration, setDuration] = useState("");

  const canSubmit = done !== null && !submitting;

  function handleSubmit() {
    if (done === null) return;

    const data: WorkoutFormData = { date, done };
    if (done && duration) {
      data.duration_minutes = Number(duration);
    }
    onSubmit(data);
  }

  return (
    <div className="flex flex-col gap-5">
      <div>
        <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
          Data
        </label>
        <input
          type="date"
          value={date}
          onChange={(e) => setDate(e.target.value)}
          className="w-full rounded-xl bg-surface border-none px-4 py-3 text-sm text-on-surface focus:ring-1 focus:ring-primary/30 focus:outline-none transition-all [color-scheme:dark]"
        />
      </div>

      <div>
        <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
          Você treinou?
        </label>
        <div className="grid grid-cols-2 gap-3">
          <button
            type="button"
            onClick={() => setDone(true)}
            className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-bold uppercase tracking-wider transition-all duration-300 ${
              done === true
                ? "bg-success text-on-primary shadow-[0_0_15px_rgba(52,211,153,0.2)]"
                : "bg-surface text-on-surface-variant hover:bg-surface-high"
            }`}
          >
            <Check size={16} />
            Fiz
          </button>
          <button
            type="button"
            onClick={() => {
              setDone(false);
              setDuration("");
            }}
            className={`flex items-center justify-center gap-2 rounded-xl px-4 py-3 text-sm font-bold uppercase tracking-wider transition-all duration-300 ${
              done === false
                ? "bg-error text-on-primary shadow-[0_0_15px_rgba(248,113,113,0.2)]"
                : "bg-surface text-on-surface-variant hover:bg-surface-high"
            }`}
          >
            <X size={16} />
            Não fiz
          </button>
        </div>
      </div>

      {done === true && (
        <div>
          <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
            Duração (minutos)
          </label>
          <input
            type="number"
            min={1}
            value={duration}
            onChange={(e) => setDuration(e.target.value)}
            placeholder="Opcional"
            className="w-full rounded-xl bg-surface border-none px-4 py-3 text-sm text-on-surface placeholder-outline focus:ring-1 focus:ring-primary/30 focus:outline-none transition-all"
          />
        </div>
      )}

      <div className="pt-2">
        <button
          type="button"
          disabled={!canSubmit}
          onClick={handleSubmit}
          className={`w-full h-14 rounded-full font-bold tracking-[0.15em] uppercase text-sm transition-all duration-300 ${
            canSubmit
              ? "bg-primary text-on-primary hover:bg-primary/90 shadow-[0_0_20px_rgba(0,206,209,0.2)]"
              : "bg-surface-high text-outline cursor-not-allowed"
          }`}
        >
          {submitting ? "Salvando..." : "Registrar"}
        </button>
      </div>
    </div>
  );
}
