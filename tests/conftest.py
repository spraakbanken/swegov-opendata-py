from pathlib import Path

import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.single_file import SingleFileAmberSnapshotExtension


@pytest.fixture
def snapshot_single(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    return snapshot.use_extension(SingleFileAmberSnapshotExtension)


@pytest.fixture()
def assets_path() -> Path:
    assets = Path(__file__).parent / "assets"
    return assets
