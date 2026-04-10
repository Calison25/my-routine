import { useNavigate } from "react-router-dom";
import { Dumbbell } from "lucide-react";

export default function LoginPage() {
  const navigate = useNavigate();

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    navigate("/treino");
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-bg px-6">
      <div className="w-full max-w-sm">
        <div className="mb-12 text-center">
          <div className="mx-auto mb-5 flex h-16 w-16 items-center justify-center rounded-full bg-primary-container">
            <Dumbbell className="h-8 w-8 text-primary" />
          </div>
          <span className="text-[10px] tracking-[0.2em] uppercase font-bold text-primary">
            Bem-vindo
          </span>
          <h1 className="mt-2 text-3xl font-extrabold tracking-tight text-on-bg">
            My Routine
          </h1>
          <p className="mt-2 text-sm text-on-surface-variant font-light">
            Acompanhe sua rotina de treinos
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
              E-mail
            </label>
            <input
              type="email"
              placeholder="seu@email.com"
              className="h-12 w-full rounded-xl bg-surface border-none px-4 text-on-surface placeholder-outline focus:ring-1 focus:ring-primary/30 focus:outline-none transition-all"
            />
          </div>
          <div>
            <label className="block text-[10px] tracking-[0.05em] uppercase font-bold text-on-surface-variant mb-2">
              Senha
            </label>
            <input
              type="password"
              placeholder="********"
              className="h-12 w-full rounded-xl bg-surface border-none px-4 text-on-surface placeholder-outline focus:ring-1 focus:ring-primary/30 focus:outline-none transition-all"
            />
          </div>
          <div className="pt-4">
            <button
              type="submit"
              className="h-14 w-full rounded-full bg-primary text-on-primary font-bold tracking-[0.15em] uppercase text-sm hover:bg-primary/90 transition-all shadow-[0_0_20px_rgba(0,206,209,0.2)]"
            >
              Entrar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
