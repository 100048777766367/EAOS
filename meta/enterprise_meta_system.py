"""Enterprise meta-system managing ontologies and taxonomies."""

from pathlib import Path

from pydantic import BaseModel, ConfigDict

ROOT_PATH = Path(__file__).resolve().parents[1]


class MetamodelGraphDTO(BaseModel):
    """Value object representing enterprise metamodel ontology graph."""

    model_config = ConfigDict(frozen=True)

    system_name: str
    entities_count: int
    triples_count: int


class EnterpriseMetaSystem:
    """Meta-system auditing enterprise architecture ontologies."""

    def __init__(self, root_path: Path | None = None) -> None:
        self.root_path: Path = root_path or ROOT_PATH

    def get_ontology_graph(self) -> MetamodelGraphDTO:
        """Retrieves structured ontology graph metadata."""
        return MetamodelGraphDTO(
            system_name="EAOS-META-ONTOLOGY",
            entities_count=38,
            triples_count=120,
        )
