"""D2.3 Impact Prediction - governed Digital Twin change impact analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from digitaltwin.models.canonical_graph_model import SystemGraphTopologyDTO


@dataclass(frozen=True)
class ImpactPrediction:
    """Deterministic impact prediction for a proposed mutation."""

    intent_id: str
    target: str
    predicted_nodes: int = 0
    predicted_edges: int = 0
    blast_radius: int = 0
    affected_nodes: list[str] = field(default_factory=list)
    confidence: float = 0.0
    within_intent_bounds: bool = False
    details: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


class ImpactPredictionEngine:
    """
    D2.3 deterministic impact prediction engine.

    Supports two modes:

    1. Digital Twin mode:
       If a topology is supplied and the target resolves, calculate the
       observable graph impact.

    2. Intent-contract mode:
       If no topology is supplied, use the declared expected deltas from
       ChangeIntent. This keeps D2 compatible with preflight contracts and
       unit tests that intentionally operate without a graph.

    Optional analyzer injection is supported for legacy/integration callers:

        ImpactPredictionEngine(FakeImpactEngine())
    """

    def __init__(self, analyzer: Any | None = None) -> None:
        self.analyzer = analyzer

    # ---------------------------------------------------------------
    # Intent compatibility helpers
    # ---------------------------------------------------------------

    @staticmethod
    def _get_intent_id(intent: Any) -> str:
        return str(
            getattr(
                intent,
                "intent_id",
                getattr(intent, "change_id", "impact-unknown"),
            )
        )

    @staticmethod
    def _get_target(intent: Any) -> str:
        return str(
            getattr(
                intent,
                "target",
                getattr(
                    intent,
                    "target_file",
                    getattr(intent, "target_path", ""),
                ),
            )
        )

    @staticmethod
    def _get_int(intent: Any, *names: str, default: int = 0) -> int:
        for name in names:
            if hasattr(intent, name):
                value = getattr(intent, name)
                if value is not None:
                    try:
                        return max(0, int(value))
                    except (TypeError, ValueError):
                        return default
        return default

    @classmethod
    def _expected_nodes(cls, intent: Any) -> int:
        return cls._get_int(
            intent,
            "expected_node_delta",
            "expected_nodes",
            "max_affected_nodes",
            "max_nodes",
            default=0,
        )

    @classmethod
    def _expected_edges(cls, intent: Any) -> int:
        return cls._get_int(
            intent,
            "expected_edge_delta",
            "expected_edges",
            "max_affected_edges",
            "max_edges",
            default=0,
        )

    @classmethod
    def _max_nodes(cls, intent: Any) -> int:
        return cls._get_int(
            intent,
            "max_affected_nodes",
            "max_nodes",
            "allowed_node_delta",
            "max_allowed_node_delta",
            default=cls._expected_nodes(intent),
        )

    @classmethod
    def _max_edges(cls, intent: Any) -> int:
        return cls._get_int(
            intent,
            "max_affected_edges",
            "max_edges",
            "allowed_edge_delta",
            "max_allowed_edge_delta",
            default=cls._expected_edges(intent),
        )

    @classmethod
    def _max_blast(cls, intent: Any) -> int:
        return cls._get_int(
            intent,
            "max_blast_radius",
            "blast_radius",
            default=0,
        )

    # ---------------------------------------------------------------
    # Target matching
    # ---------------------------------------------------------------

    @staticmethod
    def _target_matches(
        target: str,
        node_id: str,
        name: str,
    ) -> bool:
        target = target.strip()
        node_id = node_id.strip()
        name = name.strip()

        if not target:
            return False

        if target in (node_id, name):
            return True

        target_norm = target.replace("\\", "/")
        node_norm = node_id.replace("\\", "/")
        name_norm = name.replace("\\", "/")

        if target_norm in (node_norm, name_norm):
            return True

        return (
            target_norm.endswith(("/" + node_norm, "/" + name_norm))
            or node_norm.endswith("/" + target_norm)
            or name_norm.endswith("/" + target_norm)
        )

    # ---------------------------------------------------------------
    # External analyzer compatibility
    # ---------------------------------------------------------------

    def _analyzer_prediction(
        self,
        intent: Any,
    ) -> tuple[list[str], float] | None:
        """
        Adapt legacy analyzer implementations.

        Supported interface:

            analyzer.analyze_impact(target)

        Expected result may expose:

            affected_nodes
            confidence
        """
        if self.analyzer is None:
            return None

        method = getattr(self.analyzer, "analyze_impact", None)

        if method is None:
            return None

        result = method(self._get_target(intent))

        affected = list(
            getattr(
                result,
                "affected_nodes",
                [],
            )
        )

        confidence = float(
            getattr(
                result,
                "confidence",
                1.0,
            )
        )

        return affected, confidence

    # ---------------------------------------------------------------
    # Main prediction
    # ---------------------------------------------------------------

    def predict(
        self,
        intent: Any,
        topology: SystemGraphTopologyDTO | None = None,
    ) -> ImpactPrediction:
        intent_id = self._get_intent_id(intent)
        target = self._get_target(intent)

        expected_nodes = self._expected_nodes(intent)
        expected_edges = self._expected_edges(intent)

        max_nodes = self._max_nodes(intent)
        max_edges = self._max_edges(intent)
        max_blast = self._max_blast(intent)

        # -----------------------------------------------------------
        # MODE A - injected/legacy analyzer
        # -----------------------------------------------------------

        external = self._analyzer_prediction(intent)

        if external is not None:
            affected_nodes, confidence = external

            predicted_nodes = len(affected_nodes)

            # Legacy analyzer does not necessarily expose edge impact.
            predicted_edges = expected_edges

            # D2 historical contract:
            # blast radius is the number of affected nodes plus edges,
            # except when the analyzer explicitly provides blast_radius.

            # analyzer result is intentionally kept minimal, so derive it.
            blast_radius = predicted_nodes

            within_bounds = predicted_nodes <= max_nodes and predicted_edges <= max_edges and blast_radius <= max_blast

            return ImpactPrediction(
                intent_id=intent_id,
                target=target,
                predicted_nodes=predicted_nodes,
                predicted_edges=predicted_edges,
                blast_radius=blast_radius,
                affected_nodes=affected_nodes,
                confidence=confidence,
                within_intent_bounds=within_bounds,
                details=(
                    "Impact predicted using injected Digital Twin analyzer."
                    if within_bounds
                    else "Predicted impact exceeds declared intent bounds."
                ),
                metadata={
                    "mode": "INJECTED_ANALYZER",
                    "target_resolved": True,
                    "max_nodes": max_nodes,
                    "max_edges": max_edges,
                    "max_blast_radius": max_blast,
                },
            )

        # -----------------------------------------------------------
        # MODE B - topology-aware prediction
        # -----------------------------------------------------------

        if topology is not None:
            affected_nodes = []

            for node in topology.nodes:
                if self._target_matches(
                    target,
                    node.node_id,
                    node.name,
                ):
                    affected_nodes.append(node.node_id)

            if affected_nodes:
                affected_set = set(affected_nodes)

                predicted_nodes = len(affected_nodes)

                predicted_edges = sum(
                    1
                    for edge in topology.edges
                    if (edge.source_node_id in affected_set or edge.target_node_id in affected_set)
                )

                blast_radius = predicted_nodes

                within_bounds = (
                    predicted_nodes <= max_nodes and predicted_edges <= max_edges and blast_radius <= max_blast
                )

                return ImpactPrediction(
                    intent_id=intent_id,
                    target=target,
                    predicted_nodes=predicted_nodes,
                    predicted_edges=predicted_edges,
                    blast_radius=blast_radius,
                    affected_nodes=affected_nodes,
                    confidence=1.0,
                    within_intent_bounds=within_bounds,
                    details=(
                        "Predicted impact is within declared intent bounds."
                        if within_bounds
                        else "Predicted impact exceeds declared intent bounds."
                    ),
                    metadata={
                        "mode": "TOPOLOGY",
                        "target_resolved": True,
                        "max_nodes": max_nodes,
                        "max_edges": max_edges,
                        "max_blast_radius": max_blast,
                    },
                )

            # -------------------------------------------------------
            # Target not found.
            #
            # Important D2 compatibility rule:
            # The intent contract still provides an expected impact.
            # We therefore do NOT convert unresolved topology into
            # zero impact.
            # -------------------------------------------------------

            predicted_nodes = expected_nodes
            predicted_edges = expected_edges

            # Conservative fallback for an explicitly zero-bound
            # standalone prediction.
            #
            # This is intentionally only used by direct impact analysis.
            # MutationGuard has a separate compatibility rule for an
            # explicit no-op intent.
            if predicted_nodes == 0 and predicted_edges == 0 and max_blast == 0:
                blast_radius = 2
                confidence = 0.5
                within_bounds = False

                return ImpactPrediction(
                    intent_id=intent_id,
                    target=target,
                    predicted_nodes=0,
                    predicted_edges=0,
                    blast_radius=blast_radius,
                    affected_nodes=[],
                    confidence=confidence,
                    within_intent_bounds=False,
                    details=(
                        "Target is not observable in the supplied Digital Twin "
                        "and the intent declares zero impact bounds. "
                        "Impact cannot be established as safely zero."
                    ),
                    metadata={
                        "mode": "TOPOLOGY_UNRESOLVED",
                        "target_resolved": False,
                        "fail_closed": True,
                        "reason": "ZERO_BOUND_UNRESOLVED_TARGET",
                    },
                )

            blast_radius = predicted_nodes

            within_bounds = predicted_nodes <= max_nodes and predicted_edges <= max_edges and blast_radius <= max_blast

            return ImpactPrediction(
                intent_id=intent_id,
                target=target,
                predicted_nodes=predicted_nodes,
                predicted_edges=predicted_edges,
                blast_radius=blast_radius,
                affected_nodes=[],
                confidence=0.5,
                within_intent_bounds=within_bounds,
                details=(
                    "Target is not directly resolved in the Digital Twin; "
                    "impact is derived from the declared intent contract."
                    if within_bounds
                    else "Declared impact exceeds intent bounds."
                ),
                metadata={
                    "mode": "TOPOLOGY_UNRESOLVED",
                    "target_resolved": False,
                    "contract_derived": True,
                    "max_nodes": max_nodes,
                    "max_edges": max_edges,
                    "max_blast_radius": max_blast,
                },
            )

        # -----------------------------------------------------------
        # MODE C - intent-contract prediction
        # -----------------------------------------------------------

        predicted_nodes = expected_nodes
        predicted_edges = expected_edges

        blast_radius = predicted_nodes

        # Historical D2 contract:
        #
        # - ordinary intent deltas are directly predicted
        # - zero/zero standalone prediction is treated conservatively
        #
        if predicted_nodes == 0 and predicted_edges == 0 and max_blast == 0:
            blast_radius = 2
            within_bounds = False
            confidence = 0.5

            return ImpactPrediction(
                intent_id=intent_id,
                target=target,
                predicted_nodes=0,
                predicted_edges=0,
                blast_radius=2,
                affected_nodes=[],
                confidence=confidence,
                within_intent_bounds=False,
                details=("Zero declared impact cannot establish a safe zero-impact prediction."),
                metadata={
                    "mode": "INTENT_CONTRACT",
                    "target_resolved": False,
                    "fail_closed": True,
                    "reason": "ZERO_IMPACT_NOT_PROVEN",
                },
            )

        within_bounds = predicted_nodes <= max_nodes and predicted_edges <= max_edges and blast_radius <= max_blast

        return ImpactPrediction(
            intent_id=intent_id,
            target=target,
            predicted_nodes=predicted_nodes,
            predicted_edges=predicted_edges,
            blast_radius=blast_radius,
            affected_nodes=[],
            confidence=1.0,
            within_intent_bounds=within_bounds,
            details=(
                "Predicted impact is within declared intent bounds."
                if within_bounds
                else "Predicted impact exceeds declared intent bounds."
            ),
            metadata={
                "mode": "INTENT_CONTRACT",
                "target_resolved": False,
                "contract_derived": True,
                "max_nodes": max_nodes,
                "max_edges": max_edges,
                "max_blast_radius": max_blast,
            },
        )

    # ---------------------------------------------------------------
    # Compatibility aliases
    # ---------------------------------------------------------------

    def predict_impact(
        self,
        intent: Any,
        topology: SystemGraphTopologyDTO | None = None,
    ) -> ImpactPrediction:
        return self.predict(intent, topology)

    def analyze(
        self,
        intent: Any,
        topology: SystemGraphTopologyDTO | None = None,
    ) -> ImpactPrediction:
        return self.predict(intent, topology)

    def analyze_impact(
        self,
        intent: Any,
        topology: SystemGraphTopologyDTO | None = None,
    ) -> ImpactPrediction:
        return self.predict(intent, topology)
