import discord
from discord import app_commands
from discord.ext import commands
import responses
from game import Game 

client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

async def reply_to_message(bot_message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        await bot_message.author.send(response) if is_private else await bot_message.channel.send(response)
    except Exception as e:
        print(e)

async def send_message(message):
    channel = client.get_channel(1037801169847848970)
    await channel.send(message)

async def won_game():
    channel = client.get_channel(1037801169847848970)
    await channel.send(f"You won with a score of {game.score}")

async def lost_game():
    channel = client.get_channel(1037801169847848970)
    await channel.send(f"You lost with a score of {game.score}")

def run_bot():
    TOKEN = 'MTA5MjE0MDk1MTY3OTUzMzA2Ng.G0XIiJ.MfcsWnbCR-LtasZ6I0DaS381c8puhBkuGax9y0'

    # intents = discord.Intents.all()
    # intents.message_content = True
    # client = discord.Client(intents=intents)
    #client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

    @client.event
    async def on_ready():
        print(f'{client.user} is online')
        try:
            synced = await client.tree.sync()
        except Exception as e:
            print(e)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        if message.content[0] != '>':
            print("Not message to bot")
            return
        if message.channel.id != 1037801169847848970:
            print(message.channel.id)
            return
        else:
            message.content = message.content[1:]
        
        username = str(message.author)
        user_message = str(message.content)
        await reply_to_message(message, user_message, False)

    @client.tree.command(name="ping")
    async def ping(interaction: discord.Interaction):
        await interaction.response.send_message(f"pong! latency is {client.latency}")

    @client.tree.command(name="new_game")
    async def new_game(interaction: discord.Interaction):
        global game
        game = Game(interaction.user.id)
        await interaction.response.send_message(f"Creating new game!\nCurrent score: {game.score}, Type command: 'Hit' or 'Stand'?")

    @client.tree.command(name="hit")
    async def hit(interaction: discord.Interaction):
       if (game.ongoing):
           await game.hit()
           await interaction.response.send_message(f"New score: {game.score}, Hit or Stand?")
       else:
           await interaction.response.send_message("Game is over. Make new game with /new_game") 

    @client.tree.command(name="stand")
    async def stand(interaction: discord.Interaction):
        if(game.ongoing):
            await game.stand()
            await interaction.response.send_message(f"Standing. Current score: {game.score}")
        else:
           await interaction.response.send_message("Game is over. Make new game with /new_game")
        

    client.run(TOKEN)
