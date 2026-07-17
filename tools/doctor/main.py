import shutil
import subprocess
import sys


def check_command(cmd: str) -> bool:
    """Kiểm tra CLI command."""
    return shutil.which(cmd) is not None

def check_docker_container(container_name: str) -> bool:
    """Kiểm tra container Docker tương ứng."""
    try:
        result = subprocess.run(
            [
                "docker",
                "ps",
                "--filter",
                f"name={container_name}",
                "--format",
                "{{.Names}}",
            ],
            capture_output=True,
            text=True,
            check=True
        )
        return container_name in result.stdout
    except Exception:
        return False

def run_diagnostics() -> int:
    print("==========================================")
    print("      EAOS ENVIRONMENT HEALTH CHECK       ")
    print("==========================================")
    
    requirements: dict[str, bool] = {
        "Python Runtime": check_command("python"),
        "uv (Package Manager)": check_command("uv"),
        "Docker Engine": check_command("docker"),
    }

    for name, ok in requirements.items():
        status = "✅" if ok else "❌"
        print(f"{name:<25} {status}")

    print("\n--- Docker Containers Status ---")
    containers = ["eaos-postgres", "eaos-redis", "eaos-minio"]
    for container in containers:
        ok = check_docker_container(container)
        status = "✅ Active" if ok else "❌ Offline"
        print(f"{container:<25} {status}")

    print("==========================================")
    
    if not (requirements["Python Runtime"] and requirements["uv (Package Manager)"]):
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(run_diagnostics())