from pathlib import Path

root = Path(r"D:\EAOS")

adapter = root / "APPS/api/app/adapters/llm/gemini.py"
base = root / "APPS/api/app/adapters/llm/base.py"
orch = root / "APPS/api/app/services/chat/orchestrator.py"

base.write_text(
    r'''"""Abstract interface for EAOS LLM adapters."""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from typing import Any


class BaseLLMAdapter(ABC):
    """Abstract interface for streaming LLM adapters."""

    @abstractmethod
    async def generate_stream(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        json_mode: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Stream generated text."""
        raise NotImplementedError
''',
    encoding="utf-8",
)

adapter.write_text(
    r'''"""Gemini and Ollama streaming adapter."""

from __future__ import annotations

import json
import os
from collections.abc import AsyncGenerator, Iterable
from typing import Any

import httpx
from dotenv import load_dotenv

from apps.api.app.adapters.llm.base import BaseLLMAdapter

load_dotenv()


class GeminiAdapter(BaseLLMAdapter):
    """Gemini primary adapter with Ollama fallback."""

    GEMINI_URL = (
        "https://generativelanguage.googleapis.com/v1beta/models"
    )
    DEFAULT_GEMINI_MODEL = "gemini-flash-latest"
    DEFAULT_OLLAMA_URL = "http://localhost:11434"
    DEFAULT_OLLAMA_MODEL = "nemotron-mini:latest"

    def __init__(self) -> None:
        """Load provider configuration."""
        load_dotenv(override=False)

        self.provider = os.getenv(
            "DEFAULT_AI_PROVIDER",
            "gemini",
        ).strip().lower()

        self.gemini_model = os.getenv(
            "GEMINI_MODEL",
            self.DEFAULT_GEMINI_MODEL,
        ).strip()

        self.gemini_model = self.gemini_model.removeprefix("models/")

        self.ollama_url = os.getenv(
            "OLLAMA_BASE_URL",
            self.DEFAULT_OLLAMA_URL,
        ).strip().rstrip("/")

        self.ollama_model = os.getenv(
            "OLLAMA_MODEL",
            self.DEFAULT_OLLAMA_MODEL,
        ).strip()

        self.gemini_keys = self._load_keys()

        print(
            "[LLM] provider="
            f"{self.provider} "
            f"gemini_model={self.gemini_model} "
            f"gemini_keys={len(self.gemini_keys)} "
            f"ollama_model={self.ollama_model}"
        )

    @staticmethod
    def _load_keys() -> list[str]:
        """Load unique Gemini keys."""
        keys: list[str] = []

        single = os.getenv("GEMINI_API_KEY", "").strip()

        if single:
            keys.append(single)

        multiple = os.getenv("GEMINI_API_KEYS", "")

        for value in multiple.split(","):
            key = value.strip()

            if key and key not in keys:
                keys.append(key)

        return keys

    @staticmethod
    def _normalize(
        messages: Iterable[dict[str, Any]],
    ) -> list[dict[str, str]]:
        """Normalize chat messages."""
        result: list[dict[str, str]] = []

        for message in messages:
            role = str(message.get("role", "user")).strip()
            content = str(message.get("content", ""))

            if not content:
                continue

            if role not in {"system", "user", "assistant"}:
                role = "user"

            result.append(
                {
                    "role": role,
                    "content": content,
                }
            )

        return result

    @staticmethod
    def _gemini_payload(
        messages: list[dict[str, str]],
        temperature: float,
        max_output_tokens: int,
        json_mode: bool,
    ) -> dict[str, Any]:
        """Build Gemini request payload."""
        system_parts: list[str] = []
        contents: list[dict[str, Any]] = []

        for message in messages:
            role = message["role"]
            content = message["content"]

            if role == "system":
                system_parts.append(content)
                continue

            gemini_role = "model" if role == "assistant" else "user"

            contents.append(
                {
                    "role": gemini_role,
                    "parts": [{"text": content}],
                }
            )

        if not contents:
            contents = [
                {
                    "role": "user",
                    "parts": [{"text": "Hello."}],
                }
            ]

        config: dict[str, Any] = {
            "temperature": temperature,
            "maxOutputTokens": max_output_tokens,
        }

        if json_mode:
            config["responseMimeType"] = "application/json"

        payload: dict[str, Any] = {
            "contents": contents,
            "generationConfig": config,
        }

        if system_parts:
            payload["systemInstruction"] = {
                "parts": [{"text": "\n\n".join(system_parts)}],
            }

        return payload

    async def generate_stream(
        self,
        messages: list[dict[str, Any]],
        temperature: float = 0.7,
        max_output_tokens: int = 4096,
        json_mode: bool = False,
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response."""
        normalized = self._normalize(messages)

        if self.provider == "ollama":
            async for chunk in self._ollama_stream(
                normalized,
                temperature,
                max_output_tokens,
                json_mode,
            ):
                yield chunk
            return

        if not self.gemini_keys:
            raise RuntimeError(
                "GEMINI_API_KEY/GEMINI_API_KEYS is not configured."
            )

        last_error: Exception | None = None

        for index, key in enumerate(self.gemini_keys, start=1):
            try:
                print(f"[LLM] Gemini key {index}/{len(self.gemini_keys)}")

                emitted = False

                async for chunk in self._gemini_stream(
                    normalized,
                    temperature,
                    max_output_tokens,
                    json_mode,
                    key,
                ):
                    emitted = True
                    yield chunk

                if emitted:
                    print("[LLM] Gemini stream completed.")
                    return

                raise RuntimeError(
                    "Gemini returned HTTP 200 but no text content."
                )

            except Exception as exc:
                last_error = exc
                print(f"[LLM] Gemini key {index} failed: {exc}")

        print("[LLM] All Gemini keys failed.")

        if last_error is not None:
            print("[LLM] Falling back to Ollama.")

        async for chunk in self._ollama_stream(
            normalized,
            temperature,
            max_output_tokens,
            json_mode,
        ):
            yield chunk

    async def _gemini_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_output_tokens: int,
        json_mode: bool,
        api_key: str,
    ) -> AsyncGenerator[str, None]:
        """Stream Gemini SSE response."""
        payload = self._gemini_payload(
            messages,
            temperature,
            max_output_tokens,
            json_mode,
        )

        url = (
            f"{self.GEMINI_URL}/"
            f"{self.gemini_model}:streamGenerateContent"
        )

        params = {
            "key": api_key,
            "alt": "sse",
        }

        timeout = httpx.Timeout(
            connect=15.0,
            read=180.0,
            write=30.0,
            pool=30.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:
            async with client.stream(
                "POST",
                url,
                params=params,
                json=payload,
            ) as response:
                if response.status_code >= 400:
                    body = await response.aread()

                    raise RuntimeError(
                        "Gemini HTTP "
                        f"{response.status_code}: "
                        f"{body.decode('utf-8', errors='replace')}"
                    )

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    raw = line.strip()

                    if raw.startswith("data:"):
                        raw = raw[5:].strip()

                    if not raw or raw == "[DONE]":
                        continue

                    try:
                        data = json.loads(raw)
                    except json.JSONDecodeError:
                        continue

                    text = self._extract_text(data)

                    if text:
                        print(
                            f"[LLM] Gemini chunk: {len(text)} chars"
                        )
                        yield text

    @staticmethod
    def _extract_text(
        payload: dict[str, Any],
    ) -> str:
        """Extract text from a Gemini response."""
        candidates = payload.get("candidates", [])

        if not isinstance(candidates, list):
            return ""

        if not candidates:
            return ""

        candidate = candidates[0]

        if not isinstance(candidate, dict):
            return ""

        content = candidate.get("content", {})

        if not isinstance(content, dict):
            return ""

        parts = content.get("parts", [])

        if not isinstance(parts, list):
            return ""

        result: list[str] = []

        for part in parts:
            if not isinstance(part, dict):
                continue

            text = part.get("text")

            if isinstance(text, str):
                result.append(text)

        return "".join(result)

    async def _ollama_stream(
        self,
        messages: list[dict[str, str]],
        temperature: float,
        max_output_tokens: int,
        json_mode: bool,
    ) -> AsyncGenerator[str, None]:
        """Stream from local Ollama."""
        payload: dict[str, Any] = {
            "model": self.ollama_model,
            "messages": messages,
            "stream": True,
            "options": {
                "temperature": temperature,
                "num_predict": max_output_tokens,
            },
        }

        if json_mode:
            payload["format"] = "json"

        timeout = httpx.Timeout(
            connect=10.0,
            read=300.0,
            write=30.0,
            pool=30.0,
        )

        async with httpx.AsyncClient(
            timeout=timeout,
        ) as client:
            async with client.stream(
                "POST",
                f"{self.ollama_url}/api/chat",
                json=payload,
            ) as response:
                if response.status_code >= 400:
                    body = await response.aread()

                    raise RuntimeError(
                        "Ollama HTTP "
                        f"{response.status_code}: "
                        f"{body.decode('utf-8', errors='replace')}"
                    )

                async for line in response.aiter_lines():
                    if not line:
                        continue

                    try:
                        data = json.loads(line)
                    except json.JSONDecodeError:
                        continue

                    message = data.get("message", {})

                    if isinstance(message, dict):
                        content = message.get("content")

                        if isinstance(content, str) and content:
                            yield content

                    if data.get("done") is True:
                        break
''',
    encoding="utf-8",
)

orch.write_text(
    r'''"""Chat orchestrator for EAOS AI Studio."""

from __future__ import annotations

from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

from apps.api.app.adapters.llm.gemini import GeminiAdapter
from apps.api.app.services.chat.context_manager import ContextManager
from apps.api.app.services.chat.conversation_store import ConversationStore
from apps.api.app.services.chat.verification_pipeline import (
    VerificationPipeline,
)


class ChatOrchestrator:
    """Coordinate context, LLM streaming, and verification."""

    def __init__(self, project_root: Path) -> None:
        """Initialize chat services."""
        self.store = ConversationStore()
        self.context_mgr = ContextManager(project_root)
        self.llm = GeminiAdapter()
        self.verifier = VerificationPipeline(project_root)

    async def process_goal(
        self,
        conversation_id: str,
        message: str,
        system_instruction: str,
        active_file: str,
        temperature: float,
        max_output_tokens: int,
        json_mode: bool,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Process one chat request."""
        self.store.add_message(
            conversation_id,
            "user",
            message,
        )

        file_ctx = self.context_mgr.build_file_context(
            active_file,
        )

        full_system = "\n\n".join(
            part
            for part in (
                system_instruction,
                file_ctx,
            )
            if part.strip()
        )

        history = self.store.get_history(conversation_id)

        messages: list[dict[str, Any]] = []

        if full_system:
            messages.append(
                {
                    "role": "system",
                    "content": full_system,
                }
            )

        messages.extend(
            {
                "role": item.role,
                "content": item.content,
            }
            for item in history
            if item.role != "system"
        )

        yield {
            "type": "stream_start",
            "message": "LLM stream started",
        }

        full_response = ""
        chunk_count = 0

        try:
            async for token in self.llm.generate_stream(
                messages=messages,
                temperature=temperature,
                max_output_tokens=max_output_tokens,
                json_mode=json_mode,
            ):
                chunk_count += 1
                full_response += token

                yield {
                    "type": "stream_chunk",
                    "content": token,
                    "index": chunk_count,
                }

        except Exception as exc:
            yield {
                "type": "stream_error",
                "error": str(exc),
            }
            raise

        if not full_response:
            raise RuntimeError(
                "LLM returned an empty response."
            )

        self.store.add_message(
            conversation_id,
            "assistant",
            full_response,
        )

        yield {
            "type": "stream_end",
            "reply": full_response,
            "chunks": chunk_count,
        }

        yield {
            "type": "terminal_log",
            "log": "[VERIFY] Running Ruff & Pytest verification...",
        }

        verification_result = await self._run_verification()

        yield {
            "type": "stream_complete",
            "reply": full_response,
            "patch_diff": "",
            "execution_result": verification_result,
        }

    async def _run_verification(self) -> dict[str, Any]:
        """Run verification asynchronously."""
        return await self.verifier.run_checks_async()
''',
    encoding="utf-8",
)

print("[OK] Updated:")
print(f"  {base}")
print(f"  {adapter}")
print(f"  {orch}")
