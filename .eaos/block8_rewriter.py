# ruff: noqa: E501

from pathlib import Path


def rewrite(path: str, replacements: list[tuple[str, str]]) -> None:
    file = Path(path)
    text = file.read_text(encoding="utf-8")
    original = text

    for old, new in replacements:
        count = text.count(old)

        if count != 1:
            raise RuntimeError(f"{path}: expected exactly 1 match, found {count}\nFragment:\n{old}")

        text = text.replace(old, new)

    if text == original:
        raise RuntimeError(f"{path}: no changes applied")

    file.write_text(
        text,
        encoding="utf-8",
        newline="\n",
    )

    print(f"[FIX] {path}")


rewrite(
    "dxs/adapters/compatibility.py",
    [
        (
            """                reason = f"Contract versions {current} and {target} are compatible under the active policy." """.rstrip(),
            """                reason = (
                    f"Contract versions {current} and {target} "
                    "are compatible under the active policy."
                )""",
        ),
        (
            """                reason = f"Contract versions {current} and {target} are incompatible under the active policy." """.rstrip(),
            """                reason = (
                    f"Contract versions {current} and {target} "
                    "are incompatible under the active policy."
                )""",
        ),
    ],
)


rewrite(
    "dxs/ai/policy.py",
    [
        (
            """            normalized = frozenset(capability.strip() for capability in self.allowed_capabilities if capability.strip())""",
            """            normalized = frozenset(
                capability.strip()
                for capability in self.allowed_capabilities
                if capability.strip()
            )""",
        ),
    ],
)


rewrite(
    "dxs/application/ai_adapter_service.py",
    [
        (
            """            raise LookupError(f"No registered AI adapter supports capability: {request.capability}")""",
            """            raise LookupError(
                "No registered AI adapter supports "
                f"capability: {request.capability}"
            )""",
        ),
    ],
)


rewrite(
    "dxs/application/ai_policy_service.py",
    [
        (
            """                    reason=(f"Capability is not allowed by the active AI policy: {request.capability}"),""",
            """                    reason=(
                        "Capability is not allowed by the active "
                        f"AI policy: {request.capability}"
                    ),""",
        ),
        (
            """                    reason=(f"Prompt exceeds the active maximum length: {self._policy.max_prompt_length}"),""",
            """                    reason=(
                        "Prompt exceeds the active maximum length: "
                        f"{self._policy.max_prompt_length}"
                    ),""",
        ),
    ],
)


rewrite(
    "dxs/application/architecture_checker.py",
    [
        (
            """                message=("DXS root exists." if passed else f"DXS root does not exist: {self.root}"),""",
            """                message=(
                    "DXS root exists."
                    if passed
                    else f"DXS root does not exist: {self.root}"
                ),""",
        ),
        (
            """                    message=(f"Domain must not import infrastructure/framework ''{root_module}''."),""",
            """                    message=(
                        "Domain must not import infrastructure/framework "
                        f"''{root_module}''."
                    ),""",
        ),
        (
            """                    message=(f"Ports must not import infrastructure/framework ''{root_module}''."),""",
            """                    message=(
                        "Ports must not import infrastructure/framework "
                        f"''{root_module}''."
                    ),""",
        ),
        (
            """            if layer == "application" and root_module in self.APPLICATION_FORBIDDEN_IMPORTS:""",
            """            if (
                layer == "application"
                and root_module in self.APPLICATION_FORBIDDEN_IMPORTS
            ):""",
        ),
        (
            """                    message=(f"Application must not directly import infrastructure ''{root_module}''."),""",
            """                    message=(
                        "Application must not directly import "
                        f"infrastructure ''{root_module}''."
                    ),""",
        ),
        (
            """                module == forbidden or module.startswith(f"{forbidden}.") for forbidden in self.CLI_FORBIDDEN_MODULES""",
            """                (
                    module == forbidden
                    or module.startswith(f"{forbidden}.")
                )
                for forbidden in self.CLI_FORBIDDEN_MODULES""",
        ),
        (
            """                    message=(f"Application depends on outward layer {imported_layer}: {module}"),""",
            """                    message=(
                        "Application depends on outward layer "
                        f"{imported_layer}: {module}"
                    ),""",
        ),
        (
            """                print(f"PASS — {passed}/{len(results)} architecture/governance rules passed.)""".replace(
                "passed.)",
                'passed.")',
            ),
            """                print(
                    f"PASS - {passed}/{len(results)} "
                    "architecture/governance rules passed."
                )""",
        ),
    ],
)


rewrite(
    "dxs/application/repository_doctor.py",
    [
        (
            """                    results.append(f"[PASS] {document.key}: {document.path} ({document.role})")""",
            """                    results.append(
                        f"[PASS] {document.key}: "
                        f"{document.path} ({document.role})"
                    )""",
        ),
        (
            """                    results.append(f"[WARN] {document.key}: missing at {document.path} ({document.role})")""",
            """                    results.append(
                        f"[WARN] {document.key}: missing at "
                        f"{document.path} ({document.role})"
                    )""",
        ),
    ],
)


rewrite(
    "dxs/cli/main.py",
    [
        (
            """        print(f"Policy  : minor={result.policy.allow_minor_upgrade}, patch={result.policy.allow_patch_upgrade}")""",
            """        print(
            "Policy  : "
            f"minor={result.policy.allow_minor_upgrade}, "
            f"patch={result.policy.allow_patch_upgrade}"
        )""",
        ),
    ],
)


rewrite(
    "dxs/contracts/evolution.py",
    [
        (
            """                    (item for item in self.versions if item.lifecycle is ContractLifecycle.ACTIVE),""",
            """                    (
                        item
                        for item in self.versions
                        if item.lifecycle is ContractLifecycle.ACTIVE
                    ),""",
        ),
    ],
)


rewrite(
    "dxs/contracts/versioning.py",
    [
        (
            """                raise ValueError(f"Invalid contract version: {value!r}. Expected MAJOR.MINOR.PATCH.")""",
            """                raise ValueError(
                    f"Invalid contract version: {value!r}. "
                    "Expected MAJOR.MINOR.PATCH."
                )""",
        ),
    ],
)


rewrite(
    "dxs/doctor/service.py",
    [
        (
            """            level = DiagnosticLevel.INFO if result.startswith("[PASS]") else DiagnosticLevel.WARNING""",
            """            level = (
                DiagnosticLevel.INFO
                if result.startswith("[PASS]")
                else DiagnosticLevel.WARNING
            )""",
        ),
        (
            """        status = "passed" if all(diagnostic.level != DiagnosticLevel.ERROR for diagnostic in diagnostics) else "failed""",
            """        status = (
            "passed"
            if all(
                diagnostic.level != DiagnosticLevel.ERROR
                for diagnostic in diagnostics
            )
            else "failed"
        )""",
        ),
    ],
)


rewrite(
    "dxs/evolution/evidence.py",
    [
        (
            """                1 for path in root.rglob("*") if path.is_file() and ".git" not in path.parts and ".venv" not in path.parts""",
            """                1
                for path in root.rglob("*")
                if (
                    path.is_file()
                    and ".git" not in path.parts
                    and ".venv" not in path.parts
                )""",
        ),
    ],
)


rewrite(
    "dxs/migration/readiness.py",
    [
        (
            """            status = MigrationReadiness.READY if not reasons else MigrationReadiness.BLOCKED""",
            """            status = (
                MigrationReadiness.READY
                if not reasons
                else MigrationReadiness.BLOCKED
            )""",
        ),
    ],
)


rewrite(
    "tests/dxs/test_ai_policy.py",
    [
        (
            """        service = AIPolicyService(AIPolicy(allowed_capabilities=frozenset({"text-generation"})))""",
            """        service = AIPolicyService(
            AIPolicy(
                allowed_capabilities=frozenset(
                    {"text-generation"}
                )
            )
        )""",
        ),
    ],
)


rewrite(
    "tests/dxs/test_integrations.py",
    [
        (
            """        pyproject = next(check for check in result.checks if check.name == "pyproject.toml")""",
            """        pyproject = next(
            check
            for check in result.checks
            if check.name == "pyproject.toml"
        )""",
        ),
    ],
)


print("[PASS] Source rewrites completed.")
