from backend.adapters.nse_adapter import NSEAdapter
from backend.adapters.screener_adapter import ScreenerAdapter
from backend.adapters.moneycontrol_adapter import MoneycontrolAdapter
from backend.adapters.yahoo_adapter import YahooAdapter
from utils.symbol_mapper import map_symbol

class DataAggregator:

    def __init__(self):
        self.nse = NSEAdapter()
        self.screener = ScreenerAdapter()
        self.yahoo = YahooAdapter()
        self.moneycontrol = MoneycontrolAdapter()

    def fetch_all(self, symbol: str, region="IN"):

        mapped = map_symbol(symbol, region)

        results = {}

        results["nse"] = self.nse.fetch(mapped["nse"])
        results["screener"] = self.screener.fetch(mapped["screener"])
        results["yahoo"] = self.yahoo.fetch(mapped["yahoo"])
        results["moneycontrol"] = self.moneycontrol.fetch(mapped["moneycontrol"])

        return results