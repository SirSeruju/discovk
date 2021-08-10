import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegOpusAudio
from config import discord_settings, vk_settings
from vk.vkAndroidApi import VkAndroidApi
import threading
import random


def initBot(bot, urlToPlaylist, isValidUrl):
    def play(sId, voice):
        if bot.playlists[sId] == []:
            return
        else:
            event = threading.Event()
            for track in bot.playlists[sId]:
                event.clear()
                try:
                    voice.play(FFmpegOpusAudio(bot.playlists[sId][0]), after=lambda x: event.set())
                except Exception as e:
                    return
                event.wait()
                if sId in bot.playlists.keys():
                    bot.playlists[sId] = bot.playlists[sId][1:] + [bot.playlists[sId][0]]
                else:
                    return
    
    @bot.command(
        name='play',
        pass_context=True,
        description="Play the playlist with link.",
        usage="https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
    )
    async def botPlay(ctx, *args):
        if len(args) != 1:
            await ctx.send('Invalid play command, see help.')
            return
        else:
            url = args[0]
        if not isValidUrl(url):
            await ctx.send("Wrong url format, see help.")
            return
        try:
            playlist = urlToPlaylist(url)
        except Exception as e:
            await ctx.send("Invalid url.")
            return
        if not ctx.author.voice:
            await ctx.send('You have to be connected to any voice channel.')
            return
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        voice = await ctx.author.voice.channel.connect()
    
        if not voice.is_playing():
            bot.playlists[ctx.message.guild.id] = playlist
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
    async def botAdd(ctx, *args):
        if len(args) != 1:
            await ctx.send('Invalid add command, see help.')
            return
        else:
            url = args[0]
        if not isValidUrl(url):
            await ctx.send("Wrong url format, see help.")
            return
        try:
            playlist = urlToPlaylist(url)
        except Exception as e:
            await ctx.send("Invalid url.")
            return

        if not ctx.message.guild.id in bot.playlists.keys():
            await ctx.send('Current playlist is empty, use play command instead.')
            return
        if not ctx.author.voice:
            await ctx.send('You have to be connected to same voice channel.')
            return
        if not ctx.voice_client:
            await ctx.send('I have to be connected to same voice channel.')
            return
        bot.playlists[ctx.message.guild.id] += playlist
    
    @bot.command(
        name='shuffle',
        pass_context=True,
        description="Shuffle the playlist.",
    )
    async def botShuffle(ctx):
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            random.shuffle(bot.playlists[ctx.message.guild.id])
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
            bot.playlists[sId] = [bot.playlists[sId][-1]] + bot.playlists[sId][:-1]
            bot.playlists[sId] = [bot.playlists[sId][-1]] + bot.playlists[sId][:-1]
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
            del(bot.playlists[ctx.message.guild.id])
        else:
            await ctx.send('You have to be connected to the same voice channel to disconnect me.')
    

if __name__ == "__main__":
    vk = VkAndroidApi(login=vk_settings['login'], password=vk_settings['password'])
    secret, token = vk.secret, vk.token
    print("Vk - ok")

    def urlToPlaylist(url):
        owner_id, playlist_id = url.split('/')[-1].split("_")[:2]
        audios = vk.method("audio.get", owner_id=owner_id, playlist_id=playlist_id)['response']
        return list(map(lambda x: vk.to_mp3(x['url']) + "\n", audios['items']))

    def isValidUrl(url):
        prefix = '/'.join(url.split('/')[:-1])
        if (prefix == "https://vk.com/music/playlist" or prefix == "https://vk.com/music/album") and\
           len(url.split('/')[-1].split("_")) >= 2:
            return True
        else:
            return False

    bot = commands.Bot(command_prefix = discord_settings['prefix'])
    bot.playlists = {}
    initBot(bot, urlToPlaylist, isValidUrl)
    bot.run(discord_settings['token'])
