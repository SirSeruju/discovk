not_connected_to_same_channel_error = "You have to be connected to the same voice channel to %s."
not_connected_to_any_channel_error = "You have to be connected to any voice channel to %s."
already_playing_error = "Already playing audio."
invalid_usage_error = "Invalid usage, see help."
wrong_url_format_error = "Wrong url format, see help."
invalid_url_error = "Invalid url, can't reach the playlist."
translation = {
    "play": {
        "description": "Play the playlist with link.",
        "usage": "https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
        "not_connected_to_any_channel_error": not_connected_to_any_channel_error % "play",
        "already_playing_error": already_playing_error,
        "invalid_usage_error": invalid_usage_error,
        "wrong_url_format_error": wrong_url_format_error,
        "invalid_url_error": invalid_url_error,
    },
    "add": {
        "description": "Add the playlist to the queue.",
        "usage": "https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "add",
        "invalid_usage_error": invalid_usage_error,
        "wrong_url_format_error": wrong_url_format_error,
        "invalid_url_error": invalid_url_error,
        "current_playlist_is_empty": "Current playlist is empty, use play command instead.",
    },
    "stop": {
        "description": "Stop the bot.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "stop",
    },
    "next": {
        "description": "Next composition in the playlist.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "next",
    },
    "prev": {
        "description": "Previous composition in the playlist.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "prev",
    },
    "shuffle": {
        "description": "Shuffle the playlist.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "shuffle",
    },
    "resume": {
        "description": "Resume the bot where it paused.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "resume",
    },
    "pause": {
        "description": "Pause the bot.",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "pause",
    }
}
