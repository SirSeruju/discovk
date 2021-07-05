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
                del(playlists[sId])
                return
            event.wait()
            playlists[sId] = playlists[sId][1:] + [playlists[sId][0]]

@bot.command(
    name='play',
    pass_context=True,
)
async def botPlay(ctx, *args):
    global playlists
    if len(args) != 1:
        await ctx.send('Invalid play command, see help.')
        return
    else:
        url = args[0]
    if not ctx.author.voice:
        await ctx.send('You have to be connected to any voice channel.')
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
            playlists[ctx.message.guild.id] = list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))
        except Exception as e:
            await ctx.send("Wrong url, must be like: https://vk.com/music/playlist/111111111_1 or https://vk.com/music/album/111111111_1")
            return
        threading.Thread(name="player", target=play, args=(ctx.message.guild.id, voice,)).start()
    else:
        await ctx.send("Already playing audio.")
        return


@bot.command(
    name='shuffle',
    pass_context=True,
    description="shuffle the playlist",
)
async def botShuffle(ctx):
    global playlists
    random.shuffle(playlists[ctx.message.guild.id])


@bot.command(
    name='next',
    pass_context=True,
    description="next composition in the playlist",
)
async def botNext(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to next.')


@bot.command(
    name='pause',
    pass_context=True,
    description="pause bot",
)
async def botPause(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.pause()
    else:
        await ctx.send('You have to be connected to the same voice channel to pause.')


@bot.command(
    name='resume',
    pass_context=True,
    description="resume the bot where it paused",
)
async def botResume(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        ctx.voice_client.resume()
    else:
        await ctx.send('You have to be connected to the same voice channel to resume.')


@bot.command(
    name='prev',
    pass_context=True,
    description="previous composition in the playlist",
)
async def botPrev(ctx):
    sId = ctx.message.guild.id
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        playlists[sId] = [playlists[sId][-1]] + playlists[sId][:-1]
        playlists[sId] = [playlists[sId][-1]] + playlists[sId][:-1]
        ctx.voice_client.stop()
    else:
        await ctx.send('You have to be connected to the same voice channel to prev.')


@bot.command(
    name='stop',
    pass_context=True,
    description="stop the bot",
)
async def botStop(ctx):
    if ctx.author.voice.channel and ctx.author.voice.channel == ctx.voice_client.channel:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send('You have to be connected to the same voice channel to disconnect me.')


bot.run(discord_settings['token'])
