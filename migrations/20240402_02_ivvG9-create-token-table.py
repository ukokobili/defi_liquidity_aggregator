"""
create token table
"""

from yoyo import step

__depends__ = {"20240402_01_pvLdZ-create-defi-schema"}

steps = [
    step(
        """
        CREATE TABLE defi.token
        (
            token_name VARCHAR(50),
            usd NUMERIC(18, 5),
            usd_market_cap  NUMERIC(18, 5),
            usd_24h_vol NUMERIC(18, 5),
            usd_24h_change  NUMERIC(8, 5),
            last_updated_at BIGINT,
            updated_at TIMESTAMP
        )
        """,
        "DROP TABLE defi.token",
    )
]