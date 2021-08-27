import random
def add(bot, translation):
    @bot.command(
        name='shuffle',
        pass_context=True,
        description=translation["description"],
    )
    async def botShuffle(ctx):
        if ctx.author.voice and ctx.voice_client and ctx.author.voice.channel == ctx.voice_client.channel:
            random.shuffle(bot.playlists[ctx.message.guild.id])
        else:
            await ctx.send(translation["not_connected_to_same_channel_error"])
