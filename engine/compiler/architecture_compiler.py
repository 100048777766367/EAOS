from pathlib import Path
from typing import Any


class ArchitectureCompiler:
    """Động cơ Biên dịch Kiến trúc (Architecture Compiler) tối cao của EAOS."""

    def __init__(self, root_dir: Path) -> None:
        self.root_dir = root_dir
        self.output_dir = root_dir / "generated" / "compiler"

    def compile_spec(self, spec: dict[str, Any]) -> bool:
        """Biên dịch đặc tả thành mã nguồn Python, Docker, và Terraform."""
        cap_name = spec.get("capability_name", "unnamed_capability")
        target_dir = self.output_dir / cap_name

        # Tạo cấu trúc thư mục phân lớp chuẩn sạch
        dom_dir = target_dir / "domain"
        infra_dir = target_dir / "infrastructure"
        deploy_dir = target_dir / "deployment"

        dom_dir.mkdir(parents=True, exist_ok=True)
        infra_dir.mkdir(parents=True, exist_ok=True)
        deploy_dir.mkdir(parents=True, exist_ok=True)

        # 1. Biên dịch Domain Models (Pydantic Entities)
        self._compile_models(dom_dir, spec)

        # 2. Biên dịch Domain Ports (Protocols)
        self._compile_ports(dom_dir, spec)

        # 3. Biên dịch Deployment (Dockerfile & Terraform IaC)
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
            code_lines.append(
                '    """Entity tự động sinh bởi Architecture Compiler."""'
            )
            code_lines.append("")

            for f_name, f_type in fields.items():
                code_lines.append(f"    {f_name}: {f_type}")

            code_lines.append(
                "    created_at: datetime = Field("
                "default_factory=lambda: datetime.now(UTC)"
                ")"
            )
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
            "from domain.models import "
            + ", ".join([ent.get("name", "Artifact") for ent in entities]),
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
                    (
                        "    def find_by_id("
                        f"self, entity_id: str) -> {ent_name} | None: ..."
                    ),
                    "",
                ]
            )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(code_lines) + "\n")

    def _compile_deployment(self, deploy_dir: Path, spec: dict[str, Any]) -> None:
        # Biên dịch Dockerfile
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

        # Biên dịch Terraform IaC
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
