def add(bot):
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
