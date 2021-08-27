def add(bot, translation, isValidUrl, urlToPlaylist):
    @bot.command(
        name='add',
        pass_context=True,
        description=translation["description"],
        usage=translation["usage"],
    )
    async def botAdd(ctx, *args):
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

        if not ctx.message.guild.id in bot.playlists.keys():
            await ctx.send(translation["current_playlist_is_empty"])
            return
        if not ctx.author.voice:
            await ctx.send(translation["not_connected_to_same_channel_error"])
            return
        if not ctx.voice_client:
            await ctx.send(translation["not_connected_to_same_channel_error"])
            return
        bot.playlists[ctx.message.guild.id] += playlist
