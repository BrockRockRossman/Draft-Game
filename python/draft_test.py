import pytest

from teams import BUDGET_CAP, Draft, Player, add_team, draft_order


# a fresh draft with 3 teams and 3 players
def make_draft():
    teams = []  # list of Team objects
    add_team(teams, "Bears", "bears.png", 100)
    add_team(teams, "Lions", "lions.png", 100)
    add_team(teams, "Packers", "packers.png", 100)
    players = [Player("Patrick Mahomes", 15, 40),
               Player("Josh Allen", 17, 35),
               Player("Joe Burrow", 9, 30)]
    return Draft(teams, players, rounds=2)


def test_snake_order():
    teams = []
    add_team(teams, "Bears", "x", 100)
    add_team(teams, "Lions", "x", 100)
    add_team(teams, "Packers", "x", 100)
    names = []
    for team in draft_order(teams, 2):
        names.append(team.name)
    assert names == ["Bears", "Lions", "Packers", "Packers", "Lions", "Bears"]


def test_budget_cap_on_new_team():
    teams = []
    add_team(teams, "Bears", "x", BUDGET_CAP)  # exactly the cap is fine
    with pytest.raises(ValueError):
        add_team(teams, "Lions", "x", BUDGET_CAP + 1)


def test_pick_player():
    draft = make_draft()
    bears = draft.teams[0]
    assert draft.pick_player(15).name == "Patrick Mahomes"
    assert bears.budget == 60
    assert draft.current_team().name == "Lions"
    with pytest.raises(ValueError):
        draft.pick_player(15)  # already picked


def test_undo():
    draft = make_draft()
    bears = draft.teams[0]
    draft.pick_player(15)
    draft.undo_pick()
    assert bears.budget == 100
    assert bears.roster == []
    assert draft.current_team().name == "Bears"
    draft.pick_player(15)  # can be picked again
    with pytest.raises(ValueError):
        make_draft().undo_pick()  # nothing to undo


def test_trade_money():
    draft = make_draft()
    bears, lions, packers = draft.teams[0], draft.teams[1], draft.teams[2]
    draft.trade_money(bears, lions, 30)
    assert bears.budget == 70
    assert lions.budget == 130
    lions.budget = BUDGET_CAP - 10  # put the Lions right under the cap
    with pytest.raises(ValueError):
        draft.trade_money(packers, lions, 20)  # Lions would go over the cap


def test_trade_pick():
    draft = make_draft()
    lions, packers = draft.teams[1], draft.teams[2]
    draft.trade_pick(1, lions, packers)  # Lions give their first pick to the Packers
    draft.pick_player(15)
    assert draft.current_team().name == "Packers"
    with pytest.raises(ValueError):
        draft.trade_pick(0, draft.teams[0], lions)  # that pick already happened
