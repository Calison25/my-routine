import { useState } from "react";
import { ChevronLeft, ChevronRight } from "lucide-react";
import { useWorkoutCalendar } from "../../hooks/useWorkoutCalendar";
import ContributionGrid from "./ContributionGrid";
import DayDetail from "./DayDetail";
import ErrorMessage from "../../components/ErrorMessage";

const MONTH_NAMES = [
  "Janeiro", "Fevereiro", "Março", "Abril",
  "Maio", "Junho", "Julho", "Agosto",
  "Setembro", "Outubro", "Novembro", "Dezembro",
];

function SkeletonGrid() {
  return (
    <div className="grid grid-cols-7 gap-1.5">
      {Array.from({ length: 35 }, (_, i) => (
        <div
          key={i}
          className="aspect-square rounded-lg bg-surface animate-pulse"
        />
      ))}
    </div>
  );
}

export default function CalendarPage() {
  const now = new Date();
  const [month, setMonth] = useState(now.getMonth() + 1);
  const [year, setYear] = useState(now.getFullYear());
  const [selectedDate, setSelectedDate] = useState<string | null>(null);
  const { calendar, loading, error } = useWorkoutCalendar(month, year);

  function goToPreviousMonth() {
    setSelectedDate(null);
    if (month === 1) {
      setMonth(12);
      setYear((y) => y - 1);
    } else {
      setMonth((m) => m - 1);
    }
  }

  function goToNextMonth() {
    setSelectedDate(null);
    if (month === 12) {
      setMonth(1);
      setYear((y) => y + 1);
    } else {
      setMonth((m) => m + 1);
    }
  }

  function handleSelectDate(date: string) {
    setSelectedDate((prev) => (prev === date ? null : date));
  }

  return (
    <div className="px-5 py-6 max-w-lg mx-auto">
      <div className="mb-8">
        <span className="text-[10px] tracking-[0.15em] uppercase font-bold text-primary/70 block mb-1">
          Histórico
        </span>
        <h1 className="text-2xl font-extrabold tracking-tight text-on-bg">
          Calendário
        </h1>
      </div>

      <div className="flex items-center justify-between p-4 rounded-xl bg-surface mb-6">
        <button
          onClick={goToPreviousMonth}
          className="p-1.5 rounded-full text-on-surface-variant hover:text-primary transition-colors"
          aria-label="Mês anterior"
        >
          <ChevronLeft size={20} />
        </button>

        <span className="text-sm font-bold tracking-widest uppercase text-on-surface">
          {MONTH_NAMES[month - 1]} {year}
        </span>

        <button
          onClick={goToNextMonth}
          className="p-1.5 rounded-full text-on-surface-variant hover:text-primary transition-colors"
          aria-label="Próximo mês"
        >
          <ChevronRight size={20} />
        </button>
      </div>

      {error ? (
        <ErrorMessage
          message="Não foi possível carregar o calendário. Verifique se o servidor está rodando."
          onRetry={() => window.location.reload()}
        />
      ) : loading ? (
        <SkeletonGrid />
      ) : calendar ? (
        <ContributionGrid
          days={calendar.days}
          year={year}
          month={month}
          selectedDate={selectedDate}
          onSelectDate={handleSelectDate}
        />
      ) : null}

      {selectedDate && <DayDetail date={selectedDate} onClose={() => setSelectedDate(null)} />}

      <div className="flex items-center gap-6 mt-8 justify-center">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-primary/20" />
          <span className="text-[10px] tracking-wider uppercase font-bold text-on-surface-variant">Treinou</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded bg-surface" />
          <span className="text-[10px] tracking-wider uppercase font-bold text-on-surface-variant">Não treinou</span>
        </div>
      </div>
    </div>
  );
}
