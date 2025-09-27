from vulnhunter.discovery import crtsh

def test_crtsh_runs():
    res = crtsh.query_crtsh("example.com")
    assert isinstance(res, set)
