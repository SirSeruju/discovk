from discord.ext import commands
from config import discord_settings, vk_settings
from vk.vkAndroidApi import VkAndroidApi
from bot.bot import initBot

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

if __name__ == "__main__":
    vk = VkAndroidApi(login=vk_settings['login'], password=vk_settings['password'])
    secret, token = vk.secret, vk.token
    print("Vk - ok")

    bot = commands.Bot(command_prefix = discord_settings['prefix'])
    bot.playlists = {}
    initBot(bot, isValidUrl, urlToPlaylist)
    bot.run(discord_settings['token'])
