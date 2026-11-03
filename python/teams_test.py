import pytest
from teams import add_team, check_ready


def test_TwoTeams():
    teams = {}
    add_team(teams, "Bears", "", 500)
    add_team(teams, "Titans", "", 500)
    with pytest.raises(ValueError):
        check_ready(teams)


def test_threeteams():
    teams = {}
    for name in ["Bears", "Titans", "Lions"]:
        add_team(teams, name, "", 500)
    check_ready(teams)


def test_fiveteams():
    teams = {}
    for name in ["Bears", "Titans", "Lions", "Eagles", "Jets"]:
        add_team(teams, name, "", 500)
    assert len(teams) == 5


def test_sixteams():
    teams = {}
    for name in ["Bears", "Titans", "Lions", "Eagles", "Jets"]:
        add_team(teams, name, "", 500)
    with pytest.raises(ValueError):
        add_team(teams, "Giants", "", 500)


def test_negativebudget():
    with pytest.raises(ValueError):
        add_team({}, "Bears", "", -100)