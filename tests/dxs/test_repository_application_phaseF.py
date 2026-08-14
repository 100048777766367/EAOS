from dxs.bootstrap.composition import create_repository_application


def test_repository_application_contract():
    app = create_repository_application()

    assert hasattr(app, "health")
    assert hasattr(app, "evidence")
    assert hasattr(app, "remediation")
    assert hasattr(app, "scaffold")
