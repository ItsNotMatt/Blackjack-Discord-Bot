import discord
from discord import app_commands
from discord.ext import commands
import responses
import game as gm
from game import Game 

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

main_channel_id = 1037801169847848970
last_channel_id = 1037801169847848970

games = []

async def reply_to_message(bot_message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await bot_message.author.send(response) if is_private else await bot_message.channel.send(response)
    except Exception as e:
        print(e)

async def send_message(message):
    channel = client.get_channel(last_channel_id)
    await channel.send(message)

async def end_game(game: Game):
    await client.get_channel(last_channel_id).send("Game Over: Outta money")
    for i, g in enumerate(games):
        if g in games:
            games.pop(i)
            print("Games:", games)

async def won_round(game: Game):
    game.earnings()
    channel = client.get_channel(last_channel_id)
    await channel.send(f"You won this round with a score of {game.round.score}\n Money: {game.player.money}")

async def lost_round(game: Game):
    game.earnings()
    channel = client.get_channel(last_channel_id)
    await channel.send(f"You lost this round with a score of {game.round.score}\n Money: {game.player.money}")

def run_bot():
    TOKEN = ''

    @client.event
    async def on_ready():
        print(f'{client.user} is online')
        try:
            synced = await client.tree.sync()
        except Exception as e:
            print(e)

    @client.event
    async def on_message(message): #expandable to add other commands outside of / commands
        if message.author == client.user:
            return
        if message.content[0] != '>':
            print("Not message to bot")
            return
        if message.channel.id != main_channel_id:
            print(message.channel.id)
            return
        else:
            message.content = message.content[1:]
        
        username = str(message.author)
        user_message = str(message.content)
        await reply_to_message(message, user_message, False)


    @client.tree.command(name="ping")
    async def ping(interaction: discord.Interaction):
        global last_channel_id
        last_channel_id = interaction.channel_id
        await interaction.response.send_message(f"pong! latency is {client.latency}")

    @client.tree.command(name="new_game")
    async def new_game(interaction: discord.Interaction, mentioned_user: discord.Member = None):
        mentioned_id = mentioned_user.id if mentioned_user else 0 #setup to add multiplayer easily
        global last_channel_id
        last_channel_id = interaction.channel_id

        gm.del_current(interaction.user.id, games) 
        game = Game([interaction.user.id])
        games.append(game)
        await interaction.response.send_message(f"Creating new game!\nCurrent cards: {game.round.player_hand}\n"
                                    f"Dealer card: {game.round.dealer_hand[0][0]}, other card hidden.\n" 
                                    f"Type command: 'Hit' or 'Stand'?")

    @client.tree.command(name="next_round")
    async def next_round(interaction: discord.Interaction):
        global last_channel_id
        last_channel_id = interaction.channel_id

        game = gm.find_current(interaction.user.id, games)
        if game is not None and game.round.ongoing == False:
            game.next_round()#trying to switch it from next game to next round
            await interaction.response.send_message(f"Next Round:{game.round.get_hands()}")
        else:
            await interaction.response.send_message("Game not active, try /new_game")


    @client.tree.command(name="hit")
    async def hit(interaction: discord.Interaction):
        global last_channel_id
        last_channel_id = interaction.channel_id

        #need to find specific game first so multiple games can be ongoing
        game = gm.find_current(interaction.user.id, games)
        
        if game is not None and game.round.ongoing:
           await game.round.hit()
           res = game.round.get_hands()
           await interaction.response.send_message(f"{res}, Hit or Stand?")
        else:
           await interaction.response.send_message("Game is over or current round is over. use /new_game or /next_round") 

    @client.tree.command(name="stand")
    async def stand(interaction: discord.Interaction):
        global last_channel_id
        last_channel_id = interaction.channel_id
        
        game = gm.find_current(interaction.user.id, games)

        if game is not None and game.round.ongoing:
            await game.round.stand()
            await interaction.response.send_message(f"Standing. Current score: {game.round.score}")
        else:
           await interaction.response.send_message("Game is over or current round is over. use /new_game or /next_round") 
        

    client.run(TOKEN)
