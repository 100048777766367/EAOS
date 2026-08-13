import asyncio
import os
import subprocess

from google import genai

"""Production-grade Self-Healing Multi-Agent Engine with Docker Sandbox."""


# Khởi tạo Client GenAI chuẩn (Sử dụng biến môi trường GEMINI_API_KEY)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


class SystemState:
    """Bộ nhớ dùng chung của hệ thống tự cải tiến."""

    def __init__(self) -> None:
        self.system_url: str = "http://localhost:8000"
        self.logs: str = ""
        self.issue_description: str = ""
        self.proposed_code: str = ""
        self.test_results: str = ""
        self.retry_count: int = 0
        self.max_retries: int = 3
        self.is_approved: bool = False
        self.sandbox_container_id: str = "eaos-sandbox-runner"


class ObserverAgent:
    """Agent 1: Giám sát trạng thái hệ thống."""

    async def run(self, state: SystemState) -> SystemState:
        print(f"\n🔍 [Observer Agent] Đang kiểm tra hệ thống tại {state.system_url}")
        # Mô phỏng quét log hoặc trạng thái hệ thống thực tế
        state.logs = (
            "WARNING: /v1/knowledge/query Latency spike detected (1850ms). "
            "Memory leak suspected in Splay Tree Node traversal."
        )
        print(f"👉 Kết quả quan sát: {state.logs}")
        return state


class ManagerAgent:
    """Agent 2 (SẾP): Phân tích chiến lược và định hướng nhiệm vụ."""

    async def run(self, state: SystemState) -> SystemState:
        print("\n👨💼 [Manager Agent] Đang phân tích sự cố và lập kế hoạch kỹ thuật...")
        prompt = f"""
        Bạn là Kiến trúc sư trưởng hệ thống EAOS.
        Dữ liệu giám sát: {state.logs}
        Hãy phân tích nguyên nhân gốc rễ và đưa ra mệnh lệnh kỹ thuật ngắn gọn cho Coder Agent để tối ưu hóa hiệu năng.
        """
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        state.issue_description = response.text or "Tối ưu hóa thuật toán Splay Tree."
        print(f"📋 [Mệnh lệnh giao cho Coder]:\n{state.issue_description}")
        return state


class CoderAgent:
    """Agent 3: Sinh mã nguồn khắc phục sự cố."""

    async def run(self, state: SystemState) -> SystemState:
        print(f"\n💻 [Coder Agent] Đang tiến hành refactor code (Lần thử {state.retry_count + 1})...")
        prompt = f"""
        Bạn là Chuyên gia Lập trình hệ thống cấp cao.
        Nhiệm vụ: {state.issue_description}
        Phản hồi kiểm thử từ lần trước (nếu có): {state.test_results}

        Yêu cầu: Viết đoạn mã Python tối ưu. Chỉ trả về mã Python thô trong khối ```python ... ```
        """
        response = client.models.generate_content(
            model="gemini-2.5-pro",
            contents=prompt,
        )
        state.proposed_code = response.text or "# No code generated"
        print("✍️ Mã nguồn cải tiến đã được sinh thành công.")
        return state


class TesterAgent:
    """Agent 4: Kiểm thử an toàn trong Docker Sandbox."""

    async def run(self, state: SystemState) -> SystemState:
        print("\n🧪 [Tester Agent] Đang cô lập và chạy kiểm thử trong Docker Sandbox...")

        # 1. Ghi code đề xuất vào tệp tạm thời trong sandbox mount
        sandbox_path = "/tmp/eaos_sandbox_patch.py"
        clean_code = state.proposed_code
        if "```python" in clean_code:
            clean_code = clean_code.split("```python")[1].split("```")[0].strip()
        elif "```" in clean_code:
            clean_code = clean_code.split("```")[1].split("```")[0].strip()

        with open(sandbox_path, "w", encoding="utf-8") as f:
            f.write(clean_code)

        # 2. Thực thi kiểm thử thực tế qua Docker SDK / Subprocess cách ly
        try:
            cmd = [
                "docker",
                "exec",
                state.sandbox_container_id,
                "pytest",
                "/workspace/tests/unit/test_digital_twin_research.py",
            ]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=15)

            if result.returncode == 0:
                state.test_results = f"PASS: {result.stdout[-300:]}"
                print("✅ Test Sandbox thành công! Đạt chuẩn chất lượng.")
            else:
                state.test_results = f"FAIL: {result.stderr[-300:]}"
                print("❌ Test Sandbox thất bại! Phát hiện lỗi ngoại lệ.")
                state.retry_count += 1
        except Exception as e:
            # Fallback nếu Docker container chưa sẵn sàng môi trường test
            state.test_results = f"FAIL (Sandbox Exception): {e!s}"
            print(f"⚠️ Lỗi thực thi Sandbox: {e!s}")
            state.retry_count += 1

        return state


async def run_autonomous_pipeline() -> None:
    """Điều phối toàn bộ chu kỳ tự cải tiến của hệ thống."""
    state = SystemState()
    observer = ObserverAgent()
    manager = ManagerAgent()
    coder = CoderAgent()
    tester = TesterAgent()

    await observer.run(state)
    await manager.run(state)

    while state.retry_count < state.max_retries:
        await coder.run(state)
        await tester.run(state)

        if "PASS" in state.test_results:
            print("\n🎉 [HỆ THỐNG]: Cải tiến thành công! Khởi tạo Pull Request cho Human Review.")
            state.is_approved = True
            break
        print(f"⚠️ Tái định hướng vòng lặp sửa lỗi (Lần thử {state.retry_count}/{state.max_retries})")

    if not state.is_approved:
        print("\n🛑 [BẢO VỆ HỆ THỐNG]: Đã đạt giới hạn thử nghiệm. Ngắt tiến trình và gửi cảnh báo khẩn cấp.")


if __name__ == "__main__":
    asyncio.run(run_autonomous_pipeline())
