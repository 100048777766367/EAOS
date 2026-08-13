from dxs.contracts.versioning import ContractVersion
from dxs.domain.compatibility_matrix import CompatibilityMatrix


def test_matrix_is_deterministic() -> None:
    matrix = CompatibilityMatrix()

    cells = matrix.evaluate(
        (
            ContractVersion(1, 1, 0),
            ContractVersion(1, 0, 0),
        ),
        (
            ContractVersion(1, 0, 1),
            ContractVersion(2, 0, 0),
        ),
    )

    pairs = [(str(cell.current), str(cell.target), cell.compatible) for cell in cells]

    assert pairs == [
        ("1.0.0", "1.0.1", True),
        ("1.0.0", "2.0.0", False),
        ("1.1.0", "1.0.1", False),
        ("1.1.0", "2.0.0", False),
    ]
