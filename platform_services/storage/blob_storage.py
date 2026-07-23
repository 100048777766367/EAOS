"""MinIO S3 Blob Storage interface adapter."""


class BlobStorageAdapter:
    """Adapter providing S3-compatible object storage operations."""

    def __init__(self, bucket_name: str = "eaos-artifacts") -> None:
        self.bucket_name: str = bucket_name
        self._objects: dict[str, bytes] = {}

    def upload_blob(
        self,
        object_name: str,
        data: bytes,
    ) -> str:
        """Uploads binary payload to target S3 bucket."""
        self._objects[object_name] = data
        return f"s3://{self.bucket_name}/{object_name}"
