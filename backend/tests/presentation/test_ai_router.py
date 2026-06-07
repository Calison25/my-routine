from unittest.mock import AsyncMock

import pytest
from httpx import ASGITransport, AsyncClient

from app.infrastructure.ai.claude_program_generator import ProgramGeneratorService
from app.infrastructure.ai.whisper_transcription_service import (
    AudioTranscriptionService,
)
from app.main import app
from app.presentation.routers.ai import (
    get_categories_use_case,
    get_muscle_groups_use_case,
    get_program_generator_service,
    get_transcription_service,
)


# --------------- helpers ---------------

_GENERATED_PROGRAM = {
    "name": "Treino ABC",
    "slots": [
        {
            "slot_label": "Dia A",
            "categories": [{"category_id": 1, "muscle_group_id": 1}],
        },
        {
            "slot_label": "Dia B",
            "categories": [{"category_id": 1, "muscle_group_id": 4}],
        },
    ],
}


class _FakeCategory:
    def __init__(self, id: int, name: str) -> None:
        self.id = id
        self.name = name


class _FakeMuscleGroup:
    def __init__(self, id: int, name: str, category_id: int) -> None:
        self.id = id
        self.name = name
        self.category_id = category_id


# --------------- fixtures ---------------


@pytest.fixture
def mock_transcription_service() -> AsyncMock:
    service = AsyncMock(spec=AudioTranscriptionService)
    service.transcribe.return_value = "Quero treinar peito e costas"
    return service


@pytest.fixture
def mock_generator_service() -> AsyncMock:
    service = AsyncMock(spec=ProgramGeneratorService)
    service.generate.return_value = _GENERATED_PROGRAM
    return service


@pytest.fixture
def mock_categories_use_case() -> AsyncMock:
    use_case = AsyncMock()
    use_case.execute.return_value = [
        _FakeCategory(id=1, name="Musculação"),
        _FakeCategory(id=2, name="Cardio"),
    ]
    return use_case


@pytest.fixture
def mock_muscle_groups_use_case() -> AsyncMock:
    use_case = AsyncMock()
    use_case.execute.return_value = [
        _FakeMuscleGroup(id=1, name="Peito", category_id=1),
    ]
    return use_case


@pytest.fixture
def client_with_transcription_mock(mock_transcription_service: AsyncMock) -> None:
    app.dependency_overrides[get_transcription_service] = lambda: mock_transcription_service
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


@pytest.fixture
def client_with_generate_mock(
    mock_generator_service: AsyncMock,
    mock_categories_use_case: AsyncMock,
    mock_muscle_groups_use_case: AsyncMock,
) -> None:
    app.dependency_overrides[get_program_generator_service] = lambda: mock_generator_service
    app.dependency_overrides[get_categories_use_case] = lambda: mock_categories_use_case
    app.dependency_overrides[get_muscle_groups_use_case] = lambda: mock_muscle_groups_use_case
    yield  # type: ignore[misc]
    app.dependency_overrides.clear()


# --------------- tests ---------------


@pytest.mark.anyio
async def test_transcribe_returns_200_with_text(
    mock_transcription_service: AsyncMock,
    client_with_transcription_mock: None,
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/transcribe",
            files={"file": ("audio.webm", b"fake-audio-bytes", "audio/webm")},
        )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["text"] == "Quero treinar peito e costas"
    mock_transcription_service.transcribe.assert_called_once_with(
        b"fake-audio-bytes", "audio.webm"
    )


@pytest.mark.anyio
async def test_generate_program_returns_200_with_program(
    mock_generator_service: AsyncMock,
    client_with_generate_mock: None,
) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/generate-program",
            json={"transcription": "Quero treinar peito e costas"},
        )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["data"]["name"] == "Treino ABC"
    assert len(body["data"]["slots"]) == 2
    assert body["data"]["slots"][0]["slot_label"] == "Dia A"
    mock_generator_service.generate.assert_called_once()


@pytest.mark.anyio
async def test_transcribe_returns_500_on_service_error(
    mock_transcription_service: AsyncMock,
    client_with_transcription_mock: None,
) -> None:
    mock_transcription_service.transcribe.side_effect = RuntimeError("API error")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/transcribe",
            files={"file": ("audio.webm", b"fake-audio-bytes", "audio/webm")},
        )

    assert response.status_code == 500
    body = response.json()
    assert "error" in body


@pytest.mark.anyio
async def test_generate_program_returns_500_on_service_error(
    mock_generator_service: AsyncMock,
    client_with_generate_mock: None,
) -> None:
    mock_generator_service.generate.side_effect = RuntimeError("API error")
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post(
            "/api/ai/generate-program",
            json={"transcription": "Quero treinar peito e costas"},
        )

    assert response.status_code == 500
    body = response.json()
    assert "error" in body
