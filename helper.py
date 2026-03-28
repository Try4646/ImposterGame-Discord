def format_player_list(players):
    return "\n".join(f"- {player.display_name}" for player in players)

def get_game_status(game):
    return (
        f"Game ID: {game.game_id}\n"
        f"Players: {len(game.players)}\n"
        f"Status: {'Started' if game.started else 'Waiting'}\n"
        f"Creator: {game.creator.display_name}"
    )