import type { CreateProgramInput } from '../types'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001'

export async function transcribeAudio(blob: Blob): Promise<string> {
  const formData = new FormData()
  formData.append('file', blob, 'audio.webm')

  const response = await fetch(`${BASE_URL}/api/ai/transcribe`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) throw new Error('Erro na transcrição do áudio')

  const body = await response.json()
  return body.data.text
}

export async function generateProgram(
  transcription: string,
): Promise<CreateProgramInput> {
  const response = await fetch(`${BASE_URL}/api/ai/generate-program`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ transcription }),
  })

  if (!response.ok) throw new Error('Erro na geração do programa')

  const body = await response.json()
  return body.data
}
