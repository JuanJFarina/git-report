import tempfile
from pathlib import Path
from typing import Generator

import pytest


@pytest.fixture()
def folder() -> Generator[Path, None, None]:
    with tempfile.TemporaryDirectory() as directory_name:
        yield Path(directory_name)


def test_dummy() -> None: ...
