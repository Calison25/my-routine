import json
from typing import Any

import anthropic


class ProgramGeneratorService:
    """Adapter para geração de programas de treino usando Claude com tool_use."""

    SYSTEM_PROMPT = (
        "Você é um personal trainer experiente. Com base na descrição do usuário, "
        "gere um programa de treino estruturado. Use APENAS as categorias e grupos "
        "musculares fornecidos. Cada slot representa um dia de treino. "
        "Para categorias que NÃO são Musculação, não inclua muscle_group_id."
    )

    TOOL_SCHEMA: dict[str, Any] = {
        "name": "create_program",
        "description": "Cria um programa de treino estruturado",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Nome do programa de treino",
                },
                "slots": {
                    "type": "array",
                    "description": "Lista de slots (dias) do programa",
                    "items": {
                        "type": "object",
                        "properties": {
                            "slot_label": {
                                "type": "string",
                                "description": "Rótulo do slot (ex: Dia A, Segunda)",
                            },
                            "categories": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "category_id": {
                                            "type": "integer",
                                            "description": "ID da categoria de treino",
                                        },
                                        "muscle_group_id": {
                                            "type": ["integer", "null"],
                                            "description": "ID do grupo muscular (apenas para Musculação)",
                                        },
                                    },
                                    "required": ["category_id"],
                                },
                            },
                        },
                        "required": ["slot_label", "categories"],
                    },
                },
            },
            "required": ["name", "slots"],
        },
    }

    def __init__(self, api_key: str) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key)

    async def generate(
        self,
        transcription: str,
        categories: list[dict[str, Any]],
        muscle_groups: list[dict[str, Any]],
    ) -> dict[str, Any]:
        user_message = (
            f"Descrição do usuário: {transcription}\n\n"
            f"Categorias disponíveis: {json.dumps(categories, ensure_ascii=False)}\n\n"
            f"Grupos musculares disponíveis: {json.dumps(muscle_groups, ensure_ascii=False)}\n\n"
            "Gere o programa de treino usando a ferramenta create_program."
        )

        response = await self._client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=self.SYSTEM_PROMPT,
            tools=[self.TOOL_SCHEMA],
            tool_choice={"type": "tool", "name": "create_program"},
            messages=[{"role": "user", "content": user_message}],
        )

        for block in response.content:
            if block.type == "tool_use" and block.name == "create_program":
                return block.input  # type: ignore[return-value]

        raise RuntimeError("Claude não retornou a tool_use esperada")
