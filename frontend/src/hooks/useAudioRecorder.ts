import { useState, useRef, useCallback } from 'react'

type RecorderStatus = 'idle' | 'recording' | 'processing'

interface UseAudioRecorderReturn {
  status: RecorderStatus
  start: () => Promise<void>
  stop: () => void
  audioBlob: Blob | null
  error: string | null
  reset: () => void
}

export function useAudioRecorder(): UseAudioRecorderReturn {
  const [status, setStatus] = useState<RecorderStatus>('idle')
  const [audioBlob, setAudioBlob] = useState<Blob | null>(null)
  const [error, setError] = useState<string | null>(null)

  const mediaRecorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])

  const start = useCallback(async () => {
    setError(null)
    setAudioBlob(null)
    chunksRef.current = []

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm;codecs=opus')
          ? 'audio/webm;codecs=opus'
          : 'audio/webm',
      })

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunksRef.current.push(event.data)
        }
      }

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: 'audio/webm' })
        setAudioBlob(blob)
        setStatus('processing')

        for (const track of stream.getTracks()) {
          track.stop()
        }
      }

      mediaRecorderRef.current = mediaRecorder
      mediaRecorder.start()
      setStatus('recording')
    } catch {
      setError('Não foi possível acessar o microfone. Verifique as permissões.')
      setStatus('idle')
    }
  }, [])

  const stop = useCallback(() => {
    if (mediaRecorderRef.current?.state === 'recording') {
      mediaRecorderRef.current.stop()
    }
  }, [])

  const reset = useCallback(() => {
    setStatus('idle')
    setAudioBlob(null)
    setError(null)
    chunksRef.current = []
  }, [])

  return { status, start, stop, audioBlob, error, reset }
}
