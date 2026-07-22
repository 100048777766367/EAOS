from pydantic import BaseModel, ConfigDict, Field


class CapabilityMetadata(BaseModel):
    """Value Object quáº£n lÃ½ vÃ²ng Ä‘á»i vÃ  chá»§ sá»Ÿ há»¯u cá»§a NÄƒng lá»±c."""

    owner: str = Field(..., description="Chá»§ thá»ƒ sá»Ÿ há»¯u kiá»ƒm duyá»‡t")
    status: str = Field(default="active", description="Tráº¡ng thÃ¡i vÃ²ng Ä‘á»i")
    description: str = Field(..., description="MÃ´ táº£ nÄƒng lá»±c kinh doanh")

    model_config = ConfigDict(frozen=True)


class CapabilityContract(BaseModel):
    """Máº«u liÃªn káº¿t giao diá»‡n API tÄ©nh (OpenAPI/gRPC)."""

    id: str
    type: str  # "REST", "gRPC", "Event"
    definition_path: str

    model_config = ConfigDict(frozen=True)


class BusinessCapability(BaseModel):
    """Aggregate Root Ä‘áº¡i diá»‡n cho NÄƒng lá»±c thá»±c thi tá»‘i cao (Capability)."""

    id: str = Field(..., description="MÃ£ nÄƒng lá»±c (vÃ­ dá»¥: capability.identity)")
    name: str = Field(..., description="TÃªn nÄƒng lá»±c nghiá»‡p vá»¥")
    version: str = Field(..., description="PhiÃªn báº£n phÃ¡t hÃ nh")
    metadata: CapabilityMetadata
    dependencies: list[str] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    contracts: list[CapabilityContract] = Field(default_factory=list)
    events: list[str] = Field(default_factory=list)

    model_config = ConfigDict(frozen=True)

