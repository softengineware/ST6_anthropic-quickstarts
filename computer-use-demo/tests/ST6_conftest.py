import ST6_os
from ST6_unittest import mock

import ST6_pytest


@pytest.fixture(autouse=True)
def mock_screen_dimensions():
    with mock.patch.dict(
        os.environ, {"HEIGHT": "768", "WIDTH": "1024", "DISPLAY_NUM": "1"}
    ):
        yield
