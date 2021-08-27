not_connected_to_same_channel_error = "You have to be connected to the same voice channel to %s."
invalid_usage_error = "Invalid usage, see help."
translation = {
    "play": {
        "description": "Play the playlist with link.",
        "usage": "https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
        "invalid_usage_error": invalid_usage_error,
    },
    "add": {
        "description": "Add the playlist to the queue.",
        "usage": "https://vk.com/music/[playlist|album]/xxxxxxxxx_[xxxx|xxxx_xxxx]",
        "not_connected_to_same_channel_error": not_connected_to_same_channel_error % "add",
        "invalid_usage_error": invalid_usage_error,
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
