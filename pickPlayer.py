players = [
    {
        "id": 101,

        "name": "Josh Allen"
    },

    {

        "id": 102,

        "name": "Lamar Jackson"
    },

    {
        "id": 103,

        "name": "Joe Burrow"
    }

]

print("AVAILABLE PLAYERS")

for player in players:
    print("Player ID:", player["id"])

    print()

player_id = int(input("Enter the ID of the player you want to select: "))

selected_player = None

for player in players:

    if player["id"] == player_id:
        selected_player = player

        break

if selected_player is not None:

    print()

    print("PLAYER REVEALED!")

    print("Name:", selected_player["name"])

    print("Player ID:", selected_player["id"])


else:

    print("Player ID not found.")