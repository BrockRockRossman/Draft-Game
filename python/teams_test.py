import pytest
from teams import Team, Player, add_team, check_ready


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


def test_budget_goes_down():
    bears = Team("Bears", "", 500)
    bears.add_player(Player("Josh Allen", 101, 300))
    assert bears.budget == 200


def test_player_on_roster():
    bears = Team("Bears", "", 500)
    bears.add_player(Player("Josh Allen", 101, 300))
    assert bears.roster[0].name == "Josh Allen"


def test_too_expensive():
    bears = Team("Bears", "", 100)
    with pytest.raises(ValueError):
        bears.add_player(Player("Josh Allen", 101, 300))


def test_too_expensive_changes_nothing():
    bears = Team("Bears", "", 100)
    with pytest.raises(ValueError):
        bears.add_player(Player("Josh Allen", 101, 300))
    assert bears.budget == 100
    assert bears.roster == []


def test_exact_budget():
    bears = Team("Bears", "", 300)
    bears.add_player(Player("Josh Allen", 101, 300))
    assert bears.budget == 0


def test_two_players():
    bears = Team("Bears", "", 500)
    bears.add_player(Player("Josh Allen", 101, 300))
    bears.add_player(Player("Lamar Jackson", 102, 150))
    assert bears.budget == 50
    assert len(bears.roster) == 2


def test_to_dict_shows_roster():
    bears = Team("Bears", "bears.png", 500)
    bears.add_player(Player("Josh Allen", 101, 300))
    assert bears.to_dict() == {"name": "Bears", "logo": "bears.png", "budget": 200, "roster": ["Josh Allen"]}
