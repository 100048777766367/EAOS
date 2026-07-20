from packages.workflow.domain.models import WorkflowInstance


def test_workflow_instance_initialization() -> None:
    """Kiểm chứng trạng thái khởi tạo mặc định của phiên chạy."""
    instance = WorkflowInstance(
        instance_id="WF-INST-1001",
        workflow_id="workflow.invoice_approval",
    )
    assert instance.instance_id == "WF-INST-1001"
    assert instance.workflow_id == "workflow.invoice_approval"
    assert instance.current_state == "INITIALIZED"
    assert len(instance.history) == 0


def test_workflow_instance_state_transition() -> None:
    """Kiểm chứng tính đúng đắn của máy trạng thái và lưu vết lịch sử."""
    instance = WorkflowInstance(
        instance_id="WF-INST-1001",
        workflow_id="workflow.invoice_approval",
        current_state="drafted",
        history=["drafted"],
    )

    # Chuyển dịch sang trạng thái tiếp theo
    instance.transition("validating")
    assert instance.current_state == "validating"
    assert instance.history == ["drafted", "validating"]

    # Tiếp tục chuyển dịch sang trạng thái phê duyệt
    instance.transition("approved")
    assert instance.current_state == "approved"
    assert instance.history == ["drafted", "validating", "approved"]