"""Agent-economy idea intake stays linked, unscored and issuer-aware."""
from pathlib import Path

from papertrader.research_market import CALENDARS
from papertrader.research_state import read_state, validate_state

ROOT = Path(__file__).resolve().parents[2]
IDEA = "idea_ai_agent_productivity_execution_economy"
PROVIDERS = ["000660.KS","ABBN.SW","ADYEN.AS","AMD","AMZN","ANET","ASML","AVGO","BILL","CDNS","CEG","CRDO","CRWD","DDOG","ETN","GEV","GOOGL","GTLB","MA","MDB","MRVL","MSFT","MU","NET","NVDA","OKTA","ORCL","P","PANW","PRY.MI","PWR","SNOW","SNPS","STX","SU.PA","TSM","V","VRT","VST","WDC"]


def test_agent_economy_security_coverage_and_candidate_relationships():
    state = read_state(ROOT)
    assert not validate_state(ROOT, state)
    by_provider = {row["provider_symbol"]: row for row in state["securities"]}
    assert all(symbol in by_provider for symbol in PROVIDERS)
    matches = [row for row in state["relationships"] if row["idea_id"] == IDEA]
    assert len(matches) == len(PROVIDERS)
    assert {row["security_id"] for row in matches} == {
        by_provider[symbol]["security_id"] for symbol in PROVIDERS
    }
    assert all(row["status"] == "candidate" for row in matches)
    abbny = by_provider["ABBNY"]
    abbn = by_provider["ABBN.SW"]
    assert abbn["issuer_id"] == abbny["issuer_id"]
    assert abbn["security_id"] != abbny["security_id"]
    assert CALENDARS["XSWX"] == "XSWX"
    for symbol in ["000660.KS","ABBN.SW","ADYEN.AS","AMD","AVGO","BILL","CDNS","CEG","CRDO","DDOG","GTLB","MA","MDB","MRVL","MU","NET","OKTA","ORCL","P","PANW","PRY.MI","SNOW","SNPS","STX","V","VST","WDC"]:
        security = by_provider[symbol]
        assert security["research_status"] == "unresearched"
        assert security["research_role"] == "long"
        assert not any(
            row["security_id"] == security["security_id"]
            for row in state["security_assessments"]
        )
