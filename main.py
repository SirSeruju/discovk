import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegOpusAudio
from config import discord_settings, vk_settings
from vk.vkAndroidApi import VkAndroidApi
import threading
import random

vk = VkAndroidApi(login=vk_settings['login'], password=vk_settings['password'])
secret, token = vk.secret, vk.token
print("Vk - ok")

bot = commands.Bot(command_prefix = discord_settings['prefix'])
playlist = []

def play(voice):
    global playlist
    if playlist == []:
        return
    else:
        event = threading.Event()
        for track in playlist:
            event.clear()
            try:
                voice.play(FFmpegOpusAudio(playlist[0]), after=lambda x: event.set())
            except Exception as e:
                return
            event.wait()
            playlist = playlist[1:] + [playlist[0]]


@bot.command(
    name='play',
    pass_context=True,
)
async def botPlay(ctx, url):
    global playlist
    if not ctx.author.voice:
        return
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    voice = await ctx.author.voice.channel.connect()

    if not voice.is_playing():
        try:
            assert('/'.join(url.split('/')[:-1]) == "https://vk.com/music/playlist" or\
                   '/'.join(url.split('/')[:-1]) == "https://vk.com/music/album")
            assert(len(url.split('/')[-1].split('_')) == 2)
            owner_id, playlist_id = url.split('/')[-1].split("_")
            audios = vk.method("audio.get", owner_id=owner_id, playlist_id=playlist_id)['response']
            playlist = list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))
        except Exception as e:
            await ctx.send("Wrong url, must be like: https://vk.com/music/playlist/111111111_1 or https://vk.com/music/album/111111111_1")
            return
        threading.Thread(name="player", target=play, args=(voice,)).start()
    else:
        await ctx.send("Already playing audio.")
        return


@bot.command(
    name='shuffle',
    pass_context=True
)
async def botShuffle(ctx):
    global playlist
    random.shuffle(playlist)


@bot.command(
    name='next',
    pass_context=True,
)
async def botNext(ctx):
    global playlist
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to next.')


@bot.command(
    name='pause',
    pass_context=True,
)
async def botPause(ctx):
    global playlist
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.pause()
    else:
        await ctx.send('You have to be connected to the same voice channel to pause.')


@bot.command(
    name='resume',
    pass_context=True,
)
async def botResume(ctx):
    global playlist
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.resume()
    else:
        await ctx.send('You have to be connected to the same voice channel to resume.')


@bot.command(
    name='prev',
    pass_context=True,
)
async def botPrev(ctx):
    global playlist
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        playlist = [playlist[-1]] + playlist[:-1]
        playlist = [playlist[-1]] + playlist[:-1]
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to prev.')


@bot.command(
    name='stop',
    pass_context=True,
)
async def botStop(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')


bot.run(discord_settings['token'])
