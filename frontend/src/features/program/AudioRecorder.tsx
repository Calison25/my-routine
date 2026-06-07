import { useEffect } from "react";
import { Mic, Square, Loader2 } from "lucide-react";
import { useAudioRecorder } from "../../hooks/useAudioRecorder";
import { transcribeAudio, generateProgram } from "../../services/ai.service";
import type { CreateProgramInput } from "../../types";

interface AudioRecorderProps {
  onProgramGenerated: (program: CreateProgramInput) => void;
  onError: (message: string) => void;
}

export default function AudioRecorder({
  onProgramGenerated,
  onError,
}: AudioRecorderProps) {
  const { status, start, stop, audioBlob, error, reset } = useAudioRecorder();

  useEffect(() => {
    if (error) {
      onError(error);
    }
  }, [error, onError]);

  useEffect(() => {
    if (!audioBlob || status !== "processing") return;

    let cancelled = false;

    async function process() {
      try {
        const text = await transcribeAudio(audioBlob!);
        if (cancelled) return;

        const program = await generateProgram(text);
        if (cancelled) return;

        onProgramGenerated(program);
      } catch (err) {
        if (!cancelled) {
          onError(
            err instanceof Error ? err.message : "Erro ao processar áudio"
          );
        }
      } finally {
        if (!cancelled) {
          reset();
        }
      }
    }

    process();

    return () => {
      cancelled = true;
    };
  }, [audioBlob, status, onProgramGenerated, onError, reset]);

  return (
    <div className="flex flex-col items-center gap-6 py-8">
      {status === "idle" && (
        <>
          <button
            type="button"
            onClick={start}
            className="flex items-center justify-center w-24 h-24 rounded-full bg-primary text-on-primary transition-all hover:shadow-[0_0_35px_rgba(0,206,209,0.35)] active:scale-95"
            aria-label="Iniciar gravação"
          >
            <Mic size={36} />
          </button>
          <p className="text-sm text-outline font-light text-center max-w-[260px]">
            Toque para gravar e descreva seu programa de treino
          </p>
        </>
      )}

      {status === "recording" && (
        <>
          <button
            type="button"
            onClick={stop}
            className="flex items-center justify-center w-24 h-24 rounded-full bg-error text-on-primary transition-all animate-pulse active:scale-95"
            aria-label="Parar gravação"
          >
            <Square size={28} fill="currentColor" />
          </button>
          <p className="text-sm font-semibold text-error animate-pulse">
            Gravando...
          </p>
          <p className="text-xs text-outline font-light text-center max-w-[260px]">
            Descreva os treinos do seu programa. Ex: &quot;Treino A peito e
            tríceps, treino B costas e bíceps, treino C pernas e ombros&quot;
          </p>
        </>
      )}

      {status === "processing" && (
        <>
          <div className="flex items-center justify-center w-24 h-24 rounded-full bg-surface">
            <Loader2 size={36} className="text-primary animate-spin" />
          </div>
          <p className="text-sm font-semibold text-primary">
            Processando...
          </p>
          <p className="text-xs text-outline font-light">
            Transcrevendo áudio e gerando programa
          </p>
        </>
      )}
    </div>
  );
}
