"""Utility script deduplicating test functions in tests/test_eaos_master.py."""

from pathlib import Path


def deduplicate() -> None:
    p = Path("tests/test_eaos_master.py")
    if not p.exists():
        return
    lines = p.read_text(encoding="utf-8").splitlines()
    seen = set()
    cleaned = []
    skip = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("def test_hyperscale_gap"):
            fn = stripped.split("(")[0].replace("def ", "").strip()
            if fn in seen:
                skip = True
            else:
                seen.add(fn)
                skip = False

        if not skip:
            cleaned.append(line)
        elif stripped.startswith("def ") and not stripped.startswith("def test_hyperscale_gap"):
            skip = False
            cleaned.append(line)

    p.write_text("\n".join(cleaned) + "\n", encoding="utf-8")


if __name__ == "__main__":
    deduplicate()
