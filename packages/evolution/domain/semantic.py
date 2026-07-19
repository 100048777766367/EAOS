from typing import Any

from packages.evolution.domain.models import EvolutionObject


class SemanticLayer:
    """Lớp ngữ nghĩa dịch chuyển tri thức EAOS sang dạng JSON-LD và RDF."""

    @staticmethod
    def to_json_ld(obj: EvolutionObject) -> dict[str, Any]:
        """Biên dịch đối tượng sang tệp tin JSON-LD liên kết."""
        return {
            "@context": {
                "eaos": "https://eaos.internal/vocab#",
                "id": "@id",
                "type": "@type",
                "name": "eaos:name",
                "payload": "eaos:payload",
                "version": "eaos:version",
                "parent_id": "eaos:parentId",
            },
            "@type": "eaos:EvolutionObject",
            "@id": f"https://eaos.internal/objects/{obj.id}",
            "name": obj.name,
            "version": obj.payload.get("__version", 1),
            "parent_id": obj.provenance.parent_id,
            "payload": obj.payload,
        }

    @staticmethod
    def to_rdf_triples(obj: EvolutionObject) -> list[str]:
        """Biên dịch thành các bộ ba RDF (N-Triples) cho AI/AGI quét."""
        subject = f"<https://eaos.internal/objects/{obj.id}>"
        rdf_triples = [
            (
                f"{subject} "
                "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type> "
                "<https://eaos.internal/vocab#EvolutionObject> ."
            ),
            f'{subject} <https://eaos.internal/vocab#name> "{obj.name}" .',
            (
                f"{subject} <https://eaos.internal/vocab#version> "
                f'"{obj.payload.get("__version", 1)}" .'
            ),
        ]
        if obj.provenance.parent_id:
            parent_uri = f"<https://eaos.internal/objects/{obj.provenance.parent_id}>"
            rdf_triples.append(
                f"{subject} <https://eaos.internal/vocab#hasParent> {parent_uri} ."
            )
        return rdf_triples
