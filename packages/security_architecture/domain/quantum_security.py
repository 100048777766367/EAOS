import datetime
from dataclasses import dataclass, field
from enum import Enum, auto

"""
Quantum Security Domain Module.
Quản lý các đối tượng domain liên quan đến an ninh bảo mật hậu lượng tử (Post-Quantum Cryptography - PQC).
"""


class QuantumAlgorithmType(Enum):
    CRYSTALS_DILITHIUM = auto()
    CRYSTALS_KYBER = auto()
    FALCON = auto()
    SPHINCS_PLUS = auto()
    HYBRID_CLASSICAL_QUANTUM = auto()


class SecurityLevel(Enum):
    LEVEL_1 = 1  # Tương đương AES-128
    LEVEL_3 = 3  # Tương đương AES-192
    LEVEL_5 = 5  # Tương đương AES-256


@dataclass
class PostQuantumKey:
    """
    Đại diện cho Khóa Hậu Lượng Tử.

    Attributes:
        key_id (str): Định danh duy nhất của khóa.
        algorithm (QuantumAlgorithmType): Thuật toán mã hóa lượng tử sử dụng.
        security_level (SecurityLevel): Cấp độ bảo mật.
        public_key_bytes (bytes): Dữ liệu khóa công khai.
        description (str): Mô tả chi tiết mục đích và ngữ cảnh sử dụng của khóa.
        created_at (datetime.datetime): Thời điểm khởi tạo.
        is_active (bool): Trạng thái kích hoạt của khóa.
    """

    key_id: str
    algorithm: QuantumAlgorithmType
    security_level: SecurityLevel
    public_key_bytes: bytes
    description: str = ""
    created_at: datetime.datetime = field(default_factory=datetime.datetime.utcnow)
    is_active: bool = True

    def is_expired(self, max_age_days: int = 365) -> bool:
        """Kiểm tra xem khóa đã hết hạn so với thời gian quy định hay chưa."""
        now = datetime.datetime.utcnow()
        return (now - self.created_at).days > max_age_days


@dataclass
class QuantumSecurityPolicy:
    """
    Chính sách an toàn hậu lượng tử Enterprise EAOS.

    Attributes:
        policy_id (str): Mã chính sách.
        name (str): Tên chính sách.
        description (str): Mô tả chi tiết phạm vi và mục tiêu áp dụng chính sách.
        allowed_algorithms (List[QuantumAlgorithmType]): Danh sách thuật toán được cho phép.
        min_security_level (SecurityLevel): Cấp độ bảo mật tối thiểu.
        rotation_period_days (int): Chu kỳ xoay vòng khóa tính theo ngày.
        enforce_quantum_resilience (bool): Cờ bắt buộc tuân thủ chuẩn kháng lượng tử.
    """

    policy_id: str
    name: str
    description: str
    allowed_algorithms: list[QuantumAlgorithmType]
    min_security_level: SecurityLevel = SecurityLevel.LEVEL_3
    rotation_period_days: int = 90
    enforce_quantum_resilience: bool = True

    def validate_key(self, key: PostQuantumKey) -> bool:
        """Xác thực một PostQuantumKey dựa trên các tiêu chí chính sách."""
        if not key.is_active:
            return False
        if key.algorithm not in self.allowed_algorithms:
            return False
        if key.security_level.value < self.min_security_level.value:
            return False
        return not key.is_expired(self.rotation_period_days)
