def add(bot, translation):
    @bot.command(
        name='pause',
        pass_context=True,
        description=translation["description"],
    )
    async def botPause(ctx):
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            ctx.voice_client.pause()
        else:
            await ctx.send('Bot must be playing and you must be connected to the same voice channel.')
