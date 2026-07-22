import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class ArchitectureCompiler:
    """Động cơ Biên dịch Kiến trúc (Architecture Compiler) tối cao của EAOS."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.output_dir = root_dir / "generated" / "compiler"
        self.docs_dir = root_dir / "docs"

    def compile_spec(self, spec: dict[str, Any]) -> bool:
        cap_name = spec.get("capability_name", "unnamed_capability")
        target_dir = self.output_dir / cap_name

        dom_dir = target_dir / "domain"
        infra_dir = target_dir / "infrastructure"
        deploy_dir = target_dir / "deployment"

        dom_dir.mkdir(parents=True, exist_ok=True)
        infra_dir.mkdir(parents=True, exist_ok=True)
        deploy_dir.mkdir(parents=True, exist_ok=True)

        self._compile_models(dom_dir, spec)
        self._compile_ports(dom_dir, spec)
        self._compile_deployment(deploy_dir, spec)
        return True

    def _compile_models(self, dom_dir: Path, spec: dict[str, Any]) -> None:
        file_path = dom_dir / "models.py"
        entities = spec.get("entities", [])

        code_lines = [
            "from datetime import UTC, datetime",
            "from pydantic import BaseModel, ConfigDict, Field",
            "",
            "",
        ]

        for ent in entities:
            ent_name = ent.get("name", "Artifact")
            fields = ent.get("fields", {})

            code_lines.append(f"class {ent_name}(BaseModel):")
            code_lines.append('    """Entity tự động sinh bởi Architecture Compiler."""')
            code_lines.append("")

            for f_name, f_type in fields.items():
                code_lines.append(f"    {f_name}: {f_type}")

            code_lines.append("    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))")
            code_lines.append("")
            code_lines.append("    model_config = ConfigDict(frozen=True)")
            code_lines.append("")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines) + "\n")

    def _compile_ports(self, dom_dir: Path, spec: dict[str, Any]) -> None:
        file_path = dom_dir / "ports.py"
        entities = spec.get("entities", [])

        code_lines = [
            "from typing import Protocol",
            "from domain.models import " + ", ".join([ent.get("name", "Artifact") for ent in entities]),
            "",
            "",
        ]

        for ent in entities:
            ent_name = ent.get("name", "Artifact")
            code_lines.extend(
                [
                    f"class {ent_name}Repository(Protocol):",
                    '    """Port tự động sinh bởi Architecture Compiler."""',
                    "",
                    f"    def save(self, entity: {ent_name}) -> {ent_name}: ...",
                    "",
                    f"    def find_by_id(self, entity_id: str) -> {ent_name} | None: ...",
                    "",
                ]
            )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines) + "\n")

    def _compile_deployment(self, deploy_dir: Path, spec: dict[str, Any]) -> None:
        docker_file = deploy_dir / "Dockerfile"
        docker_lines = [
            "FROM python:3.11-slim",
            "WORKDIR /app",
            "COPY requirements.txt .",
            "RUN pip install --no-cache-dir -r requirements.txt",
            "COPY . .",
            'CMD ["python", "main.py"]',
        ]
        with open(docker_file, "w", encoding="utf-8") as f:
            f.write("\n".join(docker_lines) + "\n")

        tf_file = deploy_dir / "main.tf"
        cap_name = spec.get("capability_name", "unnamed_capability")
        tf_lines = [
            'provider "aws" {',
            '  region = "us-east-1"',
            "}",
            "",
            f'resource "aws_db_instance" "{cap_name}_db" {{',
            "  allocated_storage    = 20",
            '  engine               = "postgres"',
            '  instance_class       = "db.t3.micro"',
            f'  db_name              = "{cap_name}_db"',
            '  username             = "eaos"',
            '  password             = "super-secret-password"',
            "  skip_final_snapshot  = true",
            "}",
        ]
        with open(tf_file, "w", encoding="utf-8") as f:
            f.write("\n".join(tf_lines) + "\n")

    def sync_adr_index(self, adr_id: str, title: str, category: str, status: str) -> None:
        index_file = self.docs_dir / "ADR_INDEX.md"
        if not index_file.exists():
            return
        content = index_file.read_text(encoding="utf-8")
        if adr_id in content:
            return
        search_pattern = f"## {category}"
        if search_pattern in content:
            new_row = f"| {adr_id} | {title} | {category} | {status} |\n"
            parts = content.split(search_pattern)
            sub_parts = parts[1].split("\n\n", 1)
            updated_sub = sub_parts[0] + "\n" + new_row
            if len(sub_parts) > 1:
                updated_sub += "\n" + sub_parts[1]
            content = parts[0] + search_pattern + updated_sub
        with open(index_file, "w", encoding="utf-8") as f:
            f.write(content)

    def sync_current_context(self, score: int, active_packages_count: int, violations_count: int) -> None:
        ctx_file = self.docs_dir / "CURRENT_CONTEXT.md"
        if not ctx_file.exists():
            return
        content = ctx_file.read_text(encoding="utf-8")
        today_str = datetime.now(UTC).strftime("%Y-%m-%d")
        content = re.sub(r"Last Updated:\s*\d{4}-\d{2}-\d{2}", f"Last Updated: {today_str}", content)
        status_block = (
            f"Architecture Score : {score}/100\n"
            f"Active Packages    : {active_packages_count}\n"
            f"Active Violations  : {violations_count}\n"
        )
        if "=== STATUS DASHBOARD ===" in content:
            parts = content.split("=== STATUS DASHBOARD ===")
            sub_parts = parts[1].split("========================", 1)
            content = parts[0] + "=== STATUS DASHBOARD ===\n" + status_block + "========================" + sub_parts[1]
        else:
            content += f"\n\n## === STATUS DASHBOARD ===\n{status_block}========================\n"
        with open(ctx_file, "w", encoding="utf-8") as f:
            f.write(content)

    def sync_task_state(self, task_id: str, completed: bool = True) -> None:
        task_file = self.docs_dir / "TASK.md"
        if not task_file.exists():
            return
        content = task_file.read_text(encoding="utf-8")
        if completed:
            content = content.replace(f"[ ] {task_id}", f"[x] {task_id}")
        else:
            content = content.replace(f"[x] {task_id}", f"[ ] {task_id}")
        with open(task_file, "w", encoding="utf-8") as f:
            f.write(content)
