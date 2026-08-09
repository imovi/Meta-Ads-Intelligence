from scripts.data_import import load_csv, load_json, validate_rows


def test_csv_alias_normalization():
    text = "Campaign Name,Amount Spent,Impressions,Link Clicks,Purchases,Purchase Conversion Value\nSales,120,10000,200,5,300\n"
    rows = load_csv(text)
    assert rows[0]["campaign_name"] == "Sales"
    assert rows[0]["spend"] == 120.0
    assert rows[0]["clicks"] == 200.0
    assert rows[0]["conversions"] == 5.0
    assert rows[0]["revenue"] == 300.0


def test_json_data_wrapper():
    rows = load_json('{"data":[{"spend":100,"impressions":1000}]}')
    assert rows[0]["spend"] == 100.0


def test_validation_reports_missing_outcome_data():
    result = validate_rows([{"spend": 100, "impressions": 1000}])
    assert result["valid"] is True
    assert any("conversions" in warning for warning in result["warnings"])
