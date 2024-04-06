INSERT INTO defi.token (
    token_name, 
    usd, 
    usd_market_cap, 
    usd_24h_vol, 
    usd_24h_change,
    last_updated_at,
    updated_at
)
SELECT
    token_name, 
    usd, 
    usd_market_cap, 
    usd_24h_vol, 
    usd_24h_change,
    last_updated_at,
    updated_at
FROM '{{data_frame}}'