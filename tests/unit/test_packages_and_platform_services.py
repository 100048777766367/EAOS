"""Unit test suite for EAOS packages and platform services."""

from platform_services.ai.llm_adapter import LLMProviderAdapter
from platform_services.cache.distributed_cache import DistributedCacheAdapter
from platform_services.identity.sso_adapter import SSOIAMAdapter
from platform_services.storage.blob_storage import BlobStorageAdapter


def test_llm_provider_adapter() -> None:
    """Verifies LLM prompt completion abstraction."""
    adapter = LLMProviderAdapter()
    res = adapter.complete_prompt("Hello EAOS")
    assert res.model_name == "ollama/llama3"
    assert "Hello EAOS" in res.completion_text


def test_distributed_cache_adapter() -> None:
    """Verifies distributed cache set and get operations."""
    cache = DistributedCacheAdapter()
    cache.set("key1", "val1")
    assert cache.get("key1") == "val1"


def test_sso_iam_adapter() -> None:
    """Verifies SSO token authentication adapter."""
    sso = SSOIAMAdapter()
    token = sso.authenticate_token("mock_token_123")
    assert token.is_authenticated is True
    assert token.user_id == "user_sso_1001"


def test_blob_storage_adapter() -> None:
    """Verifies MinIO S3 upload adapter."""
    storage = BlobStorageAdapter("test-bucket")
    uri = storage.upload_blob("doc1.txt", b"hello world")
    assert uri == "s3://test-bucket/doc1.txt"
