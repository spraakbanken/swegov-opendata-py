
from pathlib import Path

import pytest


@pytest.fixture()
def assets_path() -> Path:
    assets = Path(__file__).parent / "assets"
    return assets
