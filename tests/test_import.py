import pytest
from pathlib import Path
import orm_ver
import os


@pytest.mark.asyncio
async def test_import_orm():
    test = Path.cwd() / 'sample_data/'
    res = await orm_ver.do_orm_import(test, False)
    assert res == True