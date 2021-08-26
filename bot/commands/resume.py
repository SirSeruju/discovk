def add(bot, translation):
    @bot.command(
        name='resume',
        pass_context=True,
        description=translation["description"],
    )
    async def botResume(ctx):
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            ctx.voice_client.resume()
        else:
            await ctx.send('You have to be connected to the same voice channel to resume.')
