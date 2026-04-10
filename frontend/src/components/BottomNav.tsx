import { NavLink } from "react-router-dom";
import { Dumbbell, Calendar } from "lucide-react";

const tabs = [
  { to: "/treino", label: "Treino", icon: Dumbbell },
  { to: "/calendario", label: "Histórico", icon: Calendar },
] as const;

export default function BottomNav() {
  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 flex items-center justify-around px-4 pb-6 pt-3 bg-bg/80 backdrop-blur-xl border-t border-outline-variant/20">
      {tabs.map(({ to, label, icon: Icon }) => (
        <NavLink
          key={to}
          to={to}
          className={({ isActive }) =>
            `flex flex-col items-center justify-center gap-1 transition-all ${
              isActive
                ? "text-primary scale-105"
                : "text-on-surface-variant hover:text-primary"
            }`
          }
        >
          <Icon size={22} />
          <span className="text-[9px] tracking-[0.1em] uppercase font-bold">
            {label}
          </span>
        </NavLink>
      ))}
    </nav>
  );
}
