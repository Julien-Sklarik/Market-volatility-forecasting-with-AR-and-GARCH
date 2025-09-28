def test_import():
    import vol_forecast
    assert hasattr(vol_forecast, 'daily_log_returns')
