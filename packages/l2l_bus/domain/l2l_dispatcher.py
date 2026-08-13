from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any, Protocol

"""L2L (Loop-to-Loop / App-to-App) Dispatcher Engine."""


class AppLoopStatus(Enum):
    """Trạng thái thực thi của Vòng lặp App."""

    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    NOT_FOUND = "NOT_FOUND"


class ExecutableAppLoopPort(Protocol):
    """Protocol bắt buộc mọi App phải tuân thủ để tham gia cơ chế L2L."""

    def __call__(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Thực thi vòng lặp phản hồi của App."""
        ...


@dataclass(frozen=True, slots=True)
class L2LCommandDTO:
    """Lệnh gọi App-to-App qua L2L Bus."""

    source_app: str
    target_app: str
    action_loop: str
    payload: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))


@dataclass(frozen=True, slots=True)
class L2LResponseDTO:
    """Kết quả phản hồi App-to-App."""

    command: L2LCommandDTO
    status: AppLoopStatus
    result_data: dict[str, Any] = field(default_factory=dict)
    error_message: str | None = None


class L2LAppDispatcher:
    """Động cơ điều phối và kích hoạt Vòng lặp giữa các Apps (L2L)."""

    def __init__(self) -> None:
        self._registered_loops: dict[str, ExecutableAppLoopPort] = {}

    def register_app_loop(self, app_name: str, loop_runner: ExecutableAppLoopPort) -> None:
        """Đăng ký vòng lặp thực thi của một App."""
        self._registered_loops[app_name] = loop_runner

    def dispatch(self, command: L2LCommandDTO) -> L2LResponseDTO:
        """Gửi lệnh gọi App-to-App L2L."""
        runner = self._registered_loops.get(command.target_app)
        if not runner:
            return L2LResponseDTO(
                command=command,
                status=AppLoopStatus.NOT_FOUND,
                error_message=(f"App Loop '{command.target_app}' không tồn tại hoặc chưa được đăng ký vào L2L Bus."),
            )

        try:
            output = runner(command.payload)
            return L2LResponseDTO(
                command=command,
                status=AppLoopStatus.SUCCESS,
                result_data=output,
            )
        except Exception as err:
            return L2LResponseDTO(
                command=command,
                status=AppLoopStatus.FAILED,
                error_message=str(err),
            )
