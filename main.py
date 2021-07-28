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
playlists = {}

def play(sId, voice):
    global playlists
    if playlists[sId] == []:
        return
    else:
        event = threading.Event()
        for track in playlists[sId]:
            event.clear()
            try:
                voice.play(FFmpegOpusAudio(playlists[sId][0]), after=lambda x: event.set())
            except Exception as e:
                return
            event.wait()
            if sId in playlists.keys():
                playlists[sId] = playlists[sId][1:] + [playlists[sId][0]]
            else:
                return


def validUrl(url):
    prefix = '/'.join(url.split('/')[:-1])
    if (prefix == "https://vk.com/music/playlist" or prefix == "https://vk.com/music/album") and\
       len(url.split('/')[-1].split("_")) >= 2:
        return True
    else:
        return False


@bot.command(
    name='play',
    pass_context=True,
    description="Play the playlist with link.",
    usage="https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
)
async def botPlay(ctx, *args):
    global playlists
    if len(args) != 1:
        await ctx.send('Invalid play command, see help.')
        return
    else:
        url = args[0]
    if not validUrl(url):
        await ctx.send("Wrong url format, see help.")
        return
    try:
        owner_id, playlist_id = url.split('/')[-1].split("_")[:2]
        audios = vk.method("audio.get", owner_id=owner_id, playlist_id=playlist_id)['response']
    except Exception as e:
        await ctx.send("Invalid url.")
        return
    if len(audios['items']) == 0:
        await ctx.send("Playlist not found.")
        return


    if not ctx.author.voice:
        await ctx.send('You have to be connected to any voice channel.')
        return
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    voice = await ctx.author.voice.channel.connect()

    if not voice.is_playing():
        playlists[ctx.message.guild.id] = list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))
        threading.Thread(name=str(ctx.message.guild.id) + "Player", target=play, args=(ctx.message.guild.id, voice,)).start()
    else:
        await ctx.send("Already playing audio.")
        return


@bot.command(
    name='add',
    pass_context=True,
    description="Add the playlist to the queue.",
    usage="https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
)
async def botPlay(ctx, *args):
    global playlists
    if len(args) != 1:
        await ctx.send('Invalid add command, see help.')
        return
    else:
        url = args[0]
    if not validUrl(url):
        await ctx.send("Wrong url format, see help.")
        return
    try:
        owner_id, playlist_id = url.split('/')[-1].split("_")[:2]
        audios = vk.method("audio.get", owner_id=owner_id, playlist_id=playlist_id)['response']
    except Exception as e:
        await ctx.send("Invalid url.")
        return
    if len(audios['items']) == 0:
        await ctx.send("Playlist not found.")
        return

    if not ctx.message.guild.id in playlists.keys():
        await ctx.send('Current playlist is empty, use play command instead.')
        return
    if not ctx.author.voice:
        await ctx.send('You have to be connected to same voice channel.')
        return
    if not ctx.voice_client:
        await ctx.send('I have to be connected to same voice channel.')
        return
    playlists[ctx.message.guild.id] += list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))

@bot.command(
    name='shuffle',
    pass_context=True,
    description="Shuffle the playlist.",
)
async def botShuffle(ctx):
    global playlists
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        random.shuffle(playlists[ctx.message.guild.id])
    else:
        await ctx.send('You have to be connected to the same voice channel to shuffle.')


@bot.command(
    name='next',
    pass_context=True,
    description="Next composition in the playlist.",
)
async def botNext(ctx):
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to next.')


@bot.command(
    name='pause',
    pass_context=True,
    description="Pause the bot.",
)
async def botPause(ctx):
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.pause()
    else:
        await ctx.send('Bot must be playing and you must be connected to the same voice channel.')


@bot.command(
    name='resume',
    pass_context=True,
    description="Resume the bot where it paused.",
)
async def botResume(ctx):
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.resume()
    else:
        await ctx.send('You have to be connected to the same voice channel to resume.')


@bot.command(
    name='prev',
    pass_context=True,
    description="Previous composition in the playlist.",
)
async def botPrev(ctx):
    sId = ctx.message.guild.id
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        playlists[sId] = [playlists[sId][-1]] + playlists[sId][:-1]
        playlists[sId] = [playlists[sId][-1]] + playlists[sId][:-1]
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to prev.')


@bot.command(
    name='stop',
    pass_context=True,
    description="Stop the bot.",
)
async def botStop(ctx):
    if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
        del(playlists[ctx.message.guild.id])
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')


bot.run(discord_settings['token'])
