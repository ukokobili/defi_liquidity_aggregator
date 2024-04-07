INSERT INTO defi.token (
    token_name, 
    usd, 
    usd_market_cap, 
    usd_24h_vol, 
    usd_24h_change,
    last_updated_at,
    updated_at
)
VALUES(
    %(token_name)s, 
    %(usd)s, 
    %(usd_market_cap)s, 
    %(usd_24h_vol)s, 
    %(usd_24h_change)s, 
    %(last_updated_at)s, 
    %(updated_at)s
);