from unittest.mock import MagicMock

from solution import (
    Company,
    get_top_10_grown,
    get_top_10_low_p_e,
    get_top_10_potential,
    get_top_10_prices,
)


def test_get_price():
    Company.__init__ = MagicMock(return_value=None)
    company = Company()
    company.dollar_rate = 100
    company.response = '{"currentValue":91.81}'
    company._get_rub_price()
    assert company.price == 9181.0


def test_get_top_10_prices():
    Company.__init__ = MagicMock(return_value=None)
    companies = [Company() for _ in range(20)]
    for i, company in enumerate(companies, start=1):
        company.price = i
        company.name = f"name_{i}"
        company.ticker = f"ticker_{i}"
    assert companies[0].price == 1
    assert companies[-1].price == 20

    top_10 = get_top_10_prices(companies)
    assert len(top_10) == 10
    assert top_10[0] == {"code": "ticker_20", "name": "name_20", "price": 20}
    assert top_10[-1] == {"code": "ticker_11", "name": "name_11", "price": 11}


def test_get_company_name_ticker():
    Company.__init__ = MagicMock(return_value=None)
    company = Company()
    company.response = '"label":"AMD (Advanced Micro Devices)  Inc.", "symbol":"AMD"'
    company._get_company_name_ticker()
    assert company.name == "AMD (Advanced Micro Devices)  Inc."
    assert company.ticker == "AMD"


def test_get_potential_profit():
    Company.__init__ = MagicMock(return_value=None)
    company = Company()
    company.response = "high52weeks: 97.98, low52weeks:  36.75"
    company._get_potential_profit()
    profit = round(97.98 * 100 / 36.75 - 100, 2)
    assert company.poten_profit == f"{profit}%"


def test_get_top_10_potential():
    Company.__init__ = MagicMock(return_value=None)
    companies = [Company() for _ in range(20)]
    for i, company in enumerate(companies, start=1):
        company.poten_profit = f"{i}%"
        company.name = f"name_{i}"
        company.ticker = f"ticker_{i}"
    assert companies[0].poten_profit == "1%"
    assert companies[-1].poten_profit == "20%"

    top_10 = get_top_10_potential(companies)
    assert len(top_10) == 10
    assert top_10[0] == {
        "code": "ticker_20",
        "name": "name_20",
        "potential profit": "20%",
    }
    assert top_10[-1] == {
        "code": "ticker_11",
        "name": "name_11",
        "potential profit": "11%",
    }


def test_get_p_e_ratio():
    Company.__init__ = MagicMock(return_value=None)
    company = Company()
    company.response = """class="snapshot__data-item"> 22.75, class="snapshot__data-item"> -35.66,
                       class="snapshot__data-item"> 55.55, class="snapshot__data-item"> 33.33,
                       class="snapshot__data-item"> 72.26"""
    company._get_p_e_ratio()
    assert company.p_e_ratio == "72.26"


def test_get_top_10_low_p_e():
    Company.__init__ = MagicMock(return_value=None)
    companies = [Company() for _ in range(20)]
    for i, company in enumerate(companies, start=1):
        company.p_e_ratio = str(float(21 - i))
        company.name = f"name_{i}"
        company.ticker = f"ticker_{i}"
    assert companies[0].p_e_ratio == "20.0"
    assert companies[-1].p_e_ratio == "1.0"

    top_10 = get_top_10_low_p_e(companies)
    assert len(top_10) == 10
    assert top_10[0] == {"code": "ticker_20", "name": "name_20", "P/E": "1.0"}
    assert top_10[-1] == {"code": "ticker_11", "name": "name_11", "P/E": "10.0"}


def test_get_one_year_index():
    Company.__init__ = MagicMock(return_value=None)
    company = Company()
    company.splited_block = ["10.73%", "-3.69", "111.17%"]
    company._get_one_year_index()
    assert company.one_year_index == "111.17%"


def test_get_top_10_grown():
    Company.__init__ = MagicMock(return_value=None)
    companies = [Company() for _ in range(20)]
    for i, company in enumerate(companies, start=1):
        company.one_year_index = f"{i}%"
        company.name = f"name_{i}"
        company.ticker = f"ticker_{i}"
    assert companies[0].one_year_index == "1%"
    assert companies[-1].one_year_index == "20%"

    top_10 = get_top_10_grown(companies)
    assert len(top_10) == 10
    assert top_10[0] == {"code": "ticker_20", "name": "name_20", "growth": "20%"}
    assert top_10[-1] == {"code": "ticker_11", "name": "name_11", "growth": "11%"}
