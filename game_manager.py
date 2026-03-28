import discord
import random
from typing import Dict, List
import Constants
import helper
import buttons
from buttons import ReadButton


class Game:
    def __init__(self, creator: discord.Member, channel: discord.TextChannel, chance: int = None):
        self.creator = creator
        self.channel = channel
        self.chance = chance
        self.players = []
        self.game_id = random.randint(1000, 9999)
        self.started = False
        self.word = None

        self.imposter = None
        self.votes = {}  # voter_id -> suspect_id
    def add_player(self, player: discord.Member):
        if player not in self.players:
            self.players.append(player)

    async def start(self, bot):
        if len(self.players) < 2:
            await self.channel.send("Need at least 3 players to start!")
            return False

        self.started = True
        c = Constants.Constants()
        if self.chance is None:
            selected_word = c.get_random_word()
        else:
            selected_word = c.chance_word(self.chance)

        self.word = selected_word["word"]
        self.hint = selected_word["hint"]
        self.imposter = random.choice(self.players)

        # Send DMs to players
        for player in self.players:
            try:
                if player == self.imposter:
                    await player.send(f"You're a ||IMPOSTER!|| The word is: ||{self.hint}||"
                                      , view=ReadButton())
                else:
                    await player.send(f"You're a ||CREWMATE!|| The word is: ||{self.word}||"
                                      , view=ReadButton())
            except discord.Forbidden:
                await self.channel.send(f"Couldn't DM {player.display_name}. Please enable DMs from server members!")

        await self.channel.send("Game started! Check your DMs for your role and word.")
        return True


class GameManager:
    def __init__(self, bot):
        self.bot = bot
        self.games: Dict[int, Game] = {}  # game_id: Game
        self.player_games: Dict[int, int] = {}  # player_id: game_id

    async def create_game(self, ctx, chance: int = None):
        if ctx.author.id in self.player_games:
            await ctx.send("You're already in a game!", delete_after=5.0)
            return
        print(chance)
        if chance is None:
            game = Game(ctx.author, ctx.channel)
            game.add_player(ctx.author)
            self.games[game.game_id] = game
            self.player_games[ctx.author.id] = game.game_id
            await ctx.send(f"Game created! ID: {game.game_id}\nOther players can join with `>join {game.game_id}`", )
        else:
            game = Game(ctx.author, ctx.channel, chance)
            game.add_player(ctx.author)
            self.games[game.game_id] = game
            self.player_games[ctx.author.id] = game.game_id
            await ctx.send(f"Game created! ID: {game.game_id}\nWith Chance for Customs of -> {chance}\nOther players can join with `>join {game.game_id}`", )


    async def join_game(self, ctx, game_id: int = None):
        if ctx.author.id in self.player_games:
            await ctx.send("You're already in a game!", delete_after=5.0)
            return

        if game_id is None:
            if not self.games:
                await ctx.send("No games available to join. Create one with `>create`", delete_after=5.0)
                return
            game = next(iter(self.games.values()))
        else:
            game = self.games.get(game_id)
            if game is None:
                await ctx.send("Game not found!", delete_after=5.0)
                return

        game.add_player(ctx.author)
        self.player_games[ctx.author.id] = game.game_id
        await ctx.send(f"{ctx.author.display_name} joined game {game.game_id}! "
                       f"Players: {len(game.players)}/{10} (use `>start` to begin)", delete_after=5.0)

    async def start_game(self, ctx):
        game_id = self.player_games.get(ctx.author.id)
        if game_id is None:
            await ctx.send("You're not in a game!", delete_after=5.0)
            return

        game = self.games.get(game_id)
        if game is None:
            await ctx.send("Game not found!", delete_after=5.0)
            return

        if game.creator != ctx.author:
            await ctx.send("Only the game creator can start the game!", delete_after=5.0)
            return

        if game.started:
            await ctx.send("Game already started!", delete_after=5.0)
            return

        await game.start(self.bot)

    async def end_game(self, ctx):
        game_id = self.player_games.get(ctx.author.id)
        if game_id is None:
            await ctx.send("You're not in a game", delete_after=5.0)
            return

        game = self.games.get(game_id)
        if game is None:
            await ctx.send("Game not found!", delete_after=5.0)
            return

        if game.creator != ctx.author:
            await ctx.send("Only the game creator can end the game!", delete_after=5.0)
            return

        # Clean up
        for player in game.players:
            self.player_games.pop(player.id, None)
        self.games.pop(game_id, None)

        await ctx.send("Game ended!", delete_after=5.0)


    async def info_game(self, ctx, game_id: int = None):
        if game_id is None:
            if not self.games:
                await ctx.send("No games available.", delete_after=5.0)
                return
            game = next(iter(self.games.values()))
        else:
            game = self.games.get(game_id)
            if game is None:
                await ctx.send("Game not found!", delete_after=5.0)
                return

        info = helper.get_game_status(game)
        await ctx.send(info)

    async def resolve_votes(self, game):
        from collections import Counter

        vote_counts = Counter(game.votes.values())
        if not vote_counts:
            await game.channel.send("No votes received.")
            return

        # Find player with most votes
        suspect_id, count = vote_counts.most_common(1)[0]
        suspect = discord.utils.get(game.channel.guild.members, id=suspect_id)

        result = f"The crew voted out {suspect.display_name}!"

        if suspect_id == game.imposter.id:
            result += "\n✅ The IMPOSTER was caught! 🎉"
        else:
            result += f"\n❌ Wrong guess. The imposter was {game.imposter.display_name}."

        await game.channel.send(result)

        for player in game.players:
            self.player_games.pop(player.id, None)
        self.games.pop(game.game_id, None)

    async def vote_player(self, ctx, player: discord.User = None):
        game_id = self.player_games.get(ctx.author.id)
        if game_id is None:
            await ctx.send("You're not in a game. retard", delete_after=5.0)
            return

        game = self.games.get(game_id)
        if not game or not game.started:
            await ctx.send("Game hasn't started or doesn't exist nigga", delete_after=5.0)
            return

        if player is None:
            await ctx.send("u didnt @ a user :thumbsup: ur such a badboy", delete_after=5.0)
            return

        if player.id not in [p.id for p in game.players]:
            await ctx.send("player not even in ur game", delete_after=5.0)
            return

        # Register vote
        game.votes[ctx.author.id] = player.id
        await ctx.send(f"{ctx.author.display_name} voted for {player.display_name}.")

        # Check if all players have voted
        if len(game.votes) == len(game.players):
            await self.resolve_votes(game)

    async def reroll_word(self, ctx):
        game_id = self.player_games.get(ctx.author.id)
        if game_id is None:
            await ctx.send("You're not in a game", delete_after=5.0)
            return

        game = self.games.get(game_id)
        if game is None:
            await ctx.send("Game not found!", delete_after=5.0)
            return

        if game.creator != ctx.author:
            await ctx.send("Only the game creator can reroll the word!", delete_after=5.0)
            return

        c = Constants.Constants()
        selected_word = c.get_random_word()
        game.word = selected_word["word"]
        game.hint = selected_word["hint"]

        for player in game.players:
            try:
                if player == game.imposter:
                    await player.send(
                        content=f"Word was rerolled! You're a ||IMPOSTER!|| Hint: ||{game.hint}||",
                        view=ReadButton()
                    )
                else:
                    await player.send(
                        content=f"Word was rerolled! You're a ||CREWMATE!|| Word: ||{game.word}||",
                        view=ReadButton()
                    )
            except discord.Forbidden:
                await game.channel.send(f"Couldn't DM {player.display_name}. Please enable DMs!")

        await game.channel.send("Word has been rerolled! Check your DMs.", delete_after=7.0)