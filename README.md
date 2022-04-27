# discovk
Discord bot for playing Vk playlists

## Run

### With kubernetes + helm
Create values.yaml and fill it with values:

    bot_id: ""
    bot_name: ""
    bot_prefix: ""
    bot_token: ""
    vk_login: ""
    vk_password: ""

then

    helm repo add discovk https://sirseruju.github.io/discovk/helm/repo
    helm install -n discovk --create-namespace -f values.yaml bot discovk/bot

### With docker-compose
Edit .env or docker-compose.yml or src/config.py, then

    docker-compose up -d
