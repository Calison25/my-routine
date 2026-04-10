import { AlertTriangle } from "lucide-react";

interface ErrorMessageProps {
  message: string;
  onRetry?: () => void;
}

export default function ErrorMessage({ message, onRetry }: ErrorMessageProps) {
  return (
    <div className="mx-4 mt-6 rounded-2xl bg-error-dim/30 p-6 text-center">
      <AlertTriangle className="mx-auto h-8 w-8 text-error" />
      <p className="mt-3 text-sm font-medium text-error">{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-4 rounded-full bg-error px-5 py-2 text-sm font-bold text-on-primary uppercase tracking-wider hover:bg-error/80 transition-colors"
        >
          Tentar novamente
        </button>
      )}
    </div>
  );
}
