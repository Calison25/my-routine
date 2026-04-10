import { Dumbbell } from "lucide-react";

export default function Header() {
  return (
    <header className="fixed top-0 left-0 right-0 z-50 flex h-14 items-center justify-between px-5 bg-bg/80 backdrop-blur-xl border-b border-outline-variant/20">
      <div className="w-8" />
      <div className="flex items-center gap-2">
        <Dumbbell size={18} className="text-primary" />
        <span className="text-sm font-bold tracking-[0.2em] uppercase text-primary">
          My Routine
        </span>
      </div>
      <div className="w-8" />
    </header>
  );
}
