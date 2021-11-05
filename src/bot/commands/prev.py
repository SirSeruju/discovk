def add(bot, translation):
    @bot.command(
        name='prev',
        pass_context=True,
        description=translation["description"],
    )
    async def botPrev(ctx):
        sId = ctx.message.guild.id
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            bot.playlists[sId] = [bot.playlists[sId][-1]] + bot.playlists[sId][:-1]
            bot.playlists[sId] = [bot.playlists[sId][-1]] + bot.playlists[sId][:-1]
            ctx.voice_client.stop()
        else:
            await ctx.send(translation["not_connected_to_same_channel_error"])
