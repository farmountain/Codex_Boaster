from backend.integrations.hipcortex_bridge import HipCortexBridge
from urllib import error
from unittest.mock import patch


def test_log_event_swallows_errors():
    bridge = HipCortexBridge(base_url="http://hipcortex")
    with patch('urllib.request.urlopen', side_effect=error.URLError('fail')) as urlopen:
        # should not raise
        bridge.log_event({"a": 1})
        urlopen.assert_called_once()


def test_fetch_snapshot_handles_error():
    bridge = HipCortexBridge(base_url="http://hipcortex")
    with patch('urllib.request.urlopen', side_effect=error.URLError('fail')):
        snap = bridge.fetch_snapshot('id')
        assert snap == {}
