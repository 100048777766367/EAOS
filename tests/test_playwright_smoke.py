def test_browser(page):
    page.goto("http://127.0.0.1:3002")
    assert page.title() is not None
