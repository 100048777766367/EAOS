from __future__ import annotations

from tools.doctor.checkers.docker_checker import DockerChecker

"""Unit test suite for Docker Checker."""


def test_docker_checker_run() -> None:
    """Test Docker checker returns DTO results."""
    checker = DockerChecker()
    checks = checker.run()
    assert len(checks) > 0
    assert checks[0].checker_id == "docker"
