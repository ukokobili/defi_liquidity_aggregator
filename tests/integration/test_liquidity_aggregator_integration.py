import csv
import datetime
from decimal import Decimal

import psycopg2

from scripts.defiliquidity.liquidity_aggregator import run_pipeline
from scripts.defiliquidity.utils.db import WarehouseConnection
from scripts.defiliquidity.utils.sde_config import get_warehouse_creds


class TestDefiLiquidity:
    def teardown_method(self, test_exchange_data_etl_run):
        with WarehouseConnection(
            get_warehouse_creds()
        ).managed_cursor() as curr:
            curr.execute("TRUNCATE TABLE defi.token;")

    def get_exchange_data(self):
        with WarehouseConnection(get_warehouse_creds()).managed_cursor(
            cursor_factory=psycopg2.extras.DictCursor
        ) as curr:
            curr.execute(
                '''SELECT id,
                        token_name, 
                        usd, 
                        usd_market_cap, 
                        usd_24h_vol, 
                        usd_24h_change,
                        last_updated_at,
                        updated_at
                    FROM defi.token;'''
            )
            table_data = [dict(r) for r in curr.fetchall()]
        return table_data

    def test_exchange_data_etl_run(self, mocker):
        mocker.patch(
            'scripts.defiliquidity.liquidity_aggregator.transform_to_add_datetime',
            return_value=[
                r
                for r in csv.DictReader(
                    open('test/fixtures/sample_raw_exchange_data.csv')
                )
            ],
        )
        run_pipeline()
        expected_result = [
            {
                'token_name': 'bitcoin',
                'usd': Decimal('67701.58286'),
                'usd_market_cap': Decimal('1331358137122.55030'),
                'usd_24h_vol': Decimal('37363439548.33762'),
                'usd_24h_change': Decimal('-0.45037'),
                'last_updated_at': 1712350829,
                'update_dt': datetime.datetime(2024, 4, 5, 21, 32, 53),
            },
            {
                'token_name': 'ethereum',
                'usd': Decimal('3337.22920'),
                'usd_market_cap': Decimal('400698176798.34880'),
                'usd_24h_vol': Decimal('16709393840.50049'),
                'usd_24h_change': Decimal('0.29586'),
                'last_updated_at': 1712350830,
                'update_dt': datetime.datetime(2024, 4, 5, 21, 32, 53),
            },
            {
                'token_name': 'marscoin',
                'usd': Decimal('0.09926'),
                'usd_market_cap': Decimal('0.00000'),
                'usd_24h_vol': Decimal('2857.279842'),
                'usd_24h_change': Decimal('-3.39411'),
                'last_updated_at': 1712349855,
                'update_dt': datetime.datetime(2024, 4, 5, 21, 32, 53),
            },
            {
                'token_name': 'solana',
                'usd': Decimal('175.92034'),
                'usd_market_cap': Decimal('78370084926.78117'),
                'usd_24h_vol': Decimal('7200557841.68512'),
                'usd_24h_change': Decimal('-3.63249'),
                'last_updated_at': 1712350824,
                'update_dt': datetime.datetime(2024, 4, 5, 21, 32, 53),
            },
        ]
        result = self.get_exchange_data()
        assert expected_result == result
