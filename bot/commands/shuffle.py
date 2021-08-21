import random
def add(bot):
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
