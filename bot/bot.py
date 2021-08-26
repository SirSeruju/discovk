from discord import FFmpegOpusAudio
import threading
import random
import bot.commands as commands

def initBot(bot, translation, isValidUrl, urlToPlaylist):
    bot.playlists = {}
    def play(sId, voice):
        if bot.playlists[sId] == []:
            return
        else:
            event = threading.Event()
            for track in bot.playlists[sId]:
                event.clear()
                try:
                    voice.play(FFmpegOpusAudio(bot.playlists[sId][0]), after=lambda x: event.set())
                except Exception as e:
                    return
                event.wait()
                if sId in bot.playlists.keys():
                    bot.playlists[sId] = bot.playlists[sId][1:] + [bot.playlists[sId][0]]
                else:
                    return
    commands.play.add(bot, translation["play"], isValidUrl, urlToPlaylist, play)
    commands.add.add(bot, translation["add"], isValidUrl, urlToPlaylist)
    commands.stop.add(bot, translation["stop"])
    commands.next.add(bot, translation["next"])
    commands.prev.add(bot, translation["prev"])
    commands.shuffle.add(bot, translation["shuffle"])
    commands.resume.add(bot, translation["resume"])
    commands.pause.add(bot, translation["pause"])
