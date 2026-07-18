# Sơ Đồ Quan Hệ Phụ Thuộc EAOS (Dependency Graph)

Bản đồ này được tự động tạo lập từ phân tích AST.

```mermaid
graph TD
    simulation["simulation"]
    self_rewrite["self_rewrite"]
    reflection["reflection"]
    prediction["prediction"]
    learning["learning"]
    learning --> reflection
    knowledge["knowledge"]
    identity["identity"]
    evolution["evolution"]
    autonomous["autonomous"]
```

