from discord import FFmpegOpusAudio
import threading

def add(bot, translation, isValidUrl, urlToPlaylist, play):
    @bot.command(
        name='play',
        pass_context=True,
        description=translation["description"],
        usage=translation["usage"],
    )
    async def botPlay(ctx, *args):
        if len(args) != 1:
            await ctx.send(translation["invalid_usage_error"])
            return
        else:
            url = args[0]
        if not isValidUrl(url):
            await ctx.send(translation["wrong_url_format_error"])
            return
        try:
            playlist = urlToPlaylist(url)
        except Exception as e:
            await ctx.send(translation["invalid_url_error"])
            return
        if not ctx.author.voice:
            await ctx.send(translation["not_connected_to_any_channel_error"])
            return
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        try:
            voice = await ctx.author.voice.channel.connect()
        except Exception as e:
            await ctx.voice_client.disconnect()
            voice = await ctx.author.voice.channel.connect()

    
        if not voice.is_playing():
            bot.playlists[ctx.message.guild.id] = playlist
            threading.Thread(name=str(ctx.message.guild.id) + "Player", target=play, args=(ctx.message.guild.id, voice,)).start()
        else:
            await ctx.send(translation["already_playing_error"])
            return
