def add(bot, translation):
    @bot.command(
        name='stop',
        pass_context=True,
        description=translation["description"],
    )
    async def botStop(ctx):
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            await ctx.voice_client.disconnect()
            del(bot.playlists[ctx.message.guild.id])
        else:
            await ctx.send(translation["not_connected_to_same_channel_error"])
