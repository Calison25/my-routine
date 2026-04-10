import type { CalendarDay } from "../../types";

interface ContributionGridProps {
  days: CalendarDay[];
  year: number;
  month: number;
  selectedDate: string | null;
  onSelectDate: (date: string) => void;
}

const WEEKDAY_LABELS = ["D", "S", "T", "Q", "Q", "S", "S"];

export default function ContributionGrid({
  days,
  year,
  month,
  selectedDate,
  onSelectDate,
}: ContributionGridProps) {
  const firstDayOfWeek = new Date(year, month - 1, 1).getDay();
  const emptySlots = Array.from({ length: firstDayOfWeek }, (_, i) => i);

  return (
    <div>
      <div className="grid grid-cols-7 gap-1.5 mb-2">
        {WEEKDAY_LABELS.map((label, i) => (
          <div
            key={i}
            className="aspect-square flex items-center justify-center text-[10px] text-outline font-bold uppercase tracking-wider"
          >
            {label}
          </div>
        ))}
      </div>

      <div className="grid grid-cols-7 gap-1.5">
        {emptySlots.map((i) => (
          <div key={`empty-${i}`} className="aspect-square" />
        ))}

        {days.map((day) => {
          const dayNumber = new Date(day.date).getUTCDate();
          const isSelected = day.date === selectedDate;

          let cellClass: string;
          if (day.done) {
            cellClass = "bg-primary/20 text-primary hover:bg-primary/30";
          } else {
            cellClass = "bg-surface text-on-surface-variant hover:bg-surface-high";
          }

          const ringClass = isSelected
            ? "ring-2 ring-primary ring-offset-1 ring-offset-bg"
            : "";

          return (
            <button
              key={day.date}
              type="button"
              data-testid={`day-${dayNumber}`}
              className={`aspect-square rounded-lg flex items-center justify-center text-xs font-medium cursor-pointer transition-all duration-200 ${cellClass} ${ringClass}`}
              title={`${dayNumber} - ${day.done ? "Treinou" : "Não treinou"} (${day.count})`}
              onClick={() => onSelectDate(day.date)}
            >
              {dayNumber}
            </button>
          );
        })}
      </div>
    </div>
  );
}
