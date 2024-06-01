import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
from pytube import YouTube
from moviepy.editor import *
import imageio
import asyncio

imageio.plugins.ffmpeg.download()  

lastMusicPlayed = str()

#inicio discord bot
load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_BOT_TOKEN')
GOOGLE_API_KEY = os.getenv('GOOGLE_KEY')
intents = discord.Intents.default()
intents.message_content = True  
bot = commands.Bot(command_prefix='h!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logado como {bot.user} (ID: {bot.user.id})')
    print('------')

#comandos

@bot.command()
async def teste(ctx):
    await ctx.send('teste')
    
@bot.command(name="play")
async def play(ctx): 
    if ctx.author.voice is None:
        await ctx.send("Você precisa estar em um canal de voz para usar este comando.")
        return

    channel = ctx.author.voice.channel
    voice = await channel.connect()
    
    url = ctx.message.content.split(" ")[1]
    
    try:
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()

        out_file = video.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp4'

        video = VideoFileClip(out_file)
        video.audio.write_audiofile(new_file)
        video.close()

        os.remove(out_file)
        print("Download concluído com sucesso:", new_file)

    except Exception as e:
        print("Ocorreu um erro:", e)

    source = discord.FFmpegPCMAudio(new_file)

    try:
        voice.play(source)
        await ctx.send(f"{new_file} tocando agora.")
        
        lastMusicPlayed = new_file
        
        print(lastMusicPlayed)

        # Aguarde até que a música termine
        while voice.is_playing():
            await asyncio.sleep(1)

    except discord.ClientException as e:
        await ctx.send(f"Erro ao tocar a música: {e}")

    finally:
        os.remove(lastMusicPlayed)

@bot.command(name="leave")
async def leave(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        await ctx.send("Saindo do canal de voz.")
    else:
        await ctx.send("Não estou conectado a nenhum canal de voz.")
        
        
        
        
import discord
import asyncio
import os
from pytube import YouTube
from moviepy.editor import *

# ... (seu código existente)

async def clean(ctx, limit=100):
    """Limpa as últimas 'limit' mensagens do canal."""
    await ctx.channel.purge(limit=limit)
    await ctx.send(f"Limpei as últimas {limit} mensagens.")


@bot.command()
async def clean(ctx, limit: int = 100):
    """Limpa as últimas mensagens do canal.

    Uso: !clean [limite]
    """
    if limit > 100:
        await ctx.send("O limite máximo é 100 mensagens.")
        return

    await ctx.channel.purge(limit=limit)  # Agora, chamamos diretamente o método purge
    await ctx.send(f"Limpei as últimas {limit} mensagens.")

# ... (resto do seu código)

bot.run(DISCORD_TOKEN)



