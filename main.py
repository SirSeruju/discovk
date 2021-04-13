import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegOpusAudio
from config import discord_settings, vk_settings
from vk.vkAndroidApi import VkAndroidApi

vk = VkAndroidApi(login=vk_settings['login'], password=vk_settings['password'])
secret, token = vk.secret, vk.token
print("Vk - ok")

bot = commands.Bot(command_prefix = discord_settings['prefix'])
playlist = []


@bot.command(
    name="set",
    pass_context=True
)
async def botSet(ctx, url):
    global playlist
    try:
        owner_id, playlist_id = url.split('/')[-1].split("_")
        audios = vk.method("audio.get", owner_id=owner_id, playlist_id=playlist_id)['response']
        playlist = list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))
    except Exception as e:
        await ctx.send("Wrong url, must be like: https://vk.com/music/playlist/111111111_1")


def play(voice):
    global playlist
    if playlist == []:
        return
    else:
        now = playlist[0]
        playlist = playlist[1:]
        voice.play(FFmpegOpusAudio(now), after=lambda x: play(voice))


@bot.command(
    name='play',
    pass_context=True,
)
async def botPlay(ctx):
    connected = ctx.author.voice
    if not connected:
        return
    voice = await connected.channel.connect()

    if not voice.is_playing():
        play(voice)
    else:
        await ctx.send("Already playing audio.")
        return


@bot.command(
    name='skip',
    pass_context=True,
)
async def botSkip(ctx):
    global playlist
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to skip.')


@bot.command(
    name='stop',
    pass_context=True,
)
async def botStop(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.stop()
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')


bot.run(discord_settings['token'])
