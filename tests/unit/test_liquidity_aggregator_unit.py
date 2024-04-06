import datetime

from scripts.defiliquidity.liquidity_aggregator import get_utc_from_unix_time


def test_get_utc_from_unix_time():
    ut: int = 1625249025588
    expected_dt = datetime.datetime(2024, 4, 5, 21, 32, 53)
    assert expected_dt == get_utc_from_unix_time(ut)
