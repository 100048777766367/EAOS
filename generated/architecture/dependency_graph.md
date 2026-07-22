# Sơ Đồ Quan Hệ Phụ Thuộc EAOS (Dependency Graph)

Bản đồ này được tự động tạo lập từ phân tích AST.

```mermaid
graph TD
    workflow["workflow"]
    traceability["traceability"]
    tenancy["tenancy"]
    specification["specification"]
    simulation["simulation"]
    self_rewrite["self_rewrite"]
    reflection["reflection"]
    prediction["prediction"]
    policy_engine["policy_engine"]
    metrics_engine["metrics_engine"]
    memory["memory"]
    marketplace["marketplace"]
    learning["learning"]
    learning --> reflection
    knowledge_graph["knowledge_graph"]
    knowledge["knowledge"]
    intelligence["intelligence"]
    identity["identity"]
    governance_loop["governance_loop"]
    feedback["feedback"]
    federation["federation"]
    exchange["exchange"]
    evolution["evolution"]
    continuous_improvement["continuous_improvement"]
    civilization["civilization"]
    capability_mapping["capability_mapping"]
    capability["capability"]
    autonomous["autonomous"]
    autonomous --> evolution
    autonomous --> learning
    autonomous --> prediction
    autonomous --> reflection
    autonomous --> self_rewrite
    autonomous --> simulation
    autonomous --> workflow
    architecture_memory["architecture_memory"]
    architecture_fitness["architecture_fitness"]
    agent["agent"]
```

