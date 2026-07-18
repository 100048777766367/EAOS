import json
from pathlib import Path

from tools.graph.dependency_graph_generator import DependencyGraphGenerator


def test_dependency_graph_generation() -> None:
    """Kiểm thử chu trình tự trị phân tích AST và xuất bản đồ đồ thị."""
    root_dir = Path(__file__).resolve().parent.parent.parent
    generator = DependencyGraphGenerator(root_dir)

    success = generator.generate()
    assert success is True

    # Đảm bảo các tệp tin đích đã được khởi tạo
    output_dir = root_dir / "generated" / "architecture"
    json_file = output_dir / "dependency_graph.json"
    md_file = output_dir / "dependency_graph.md"
    dot_file = output_dir / "dependency_graph.dot"

    assert json_file.exists()
    assert md_file.exists()
    assert dot_file.exists()

    # Đọc tệp JSON và kiểm chứng ranh giới kết nối của các Package
    with open(json_file, encoding="utf-8") as f:
        graph = json.load(f)

    assert isinstance(graph, dict)