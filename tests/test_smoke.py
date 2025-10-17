def test_app_imports():
    import importlib.util
    import pathlib
    app_path = pathlib.Path("dashboard.py") 
    spec = importlib.util.spec_from_file_location("app", app_path)
    assert spec is not None, "Could not find dashboard.py"