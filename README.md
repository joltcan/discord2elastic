# discord2elastic aka log2elastic

Sometimes you want chatlogs to be searchable. Put them in elasticsearch and keep em!

## Setup

discord2elastic runs by itself. Set the environment variables and go ahead. 

You first need a discord user, see the [Discord bot](#Discord-bot) topic for reference. 

You also need an [elasticsearch](#Elasticsearch) user that can create index and documents.

Run it manually or use the [ansible playbook](#Ansible-playbook):

```
export ELASTICSEARCH_INDEX="discord_log"
export ELASTICSEARCH_URL="https://elastic:9200"
export BOT_TOKEN="<sometoken>"

docker run \
	--rm \
	--detach \
    -e ELASTICSEARCH_INDEX=${ELASTICSEARCH_INDEX} \
    -e ELASTICSEARCH_URL=${ELASTICSEARCH_URL} \
    -e BOT_TOKEN=${BOT_TOKEN} \
	--hostname=discord2elastic \
	--name=discord2elastic \
	jolt/discord2elastic
```
## note

Port is _mandatory_ in `ELASTICSEARCH_URL`.

The docker runs as `USER nobody`.

Add an additional `DEBUG=1` if you want logging.

## Discord bot

1. Make an application [here](https://discord.com/developers/applications)  and name it `log2elastic` or whatever you prefer. Due to Discord rules the name can not contain `discord`.
2  Under `General Information`, copy the `APPLICATION ID`.
2. Navigate to `bot` and enable it, and copy the `TOKEN`. This is used for the `BOT_TOKEN` variable.
3  Still under `bot`scroll down and enable "Messsage Content Intent" under `Privileged Gateway Intents`
4. Use the following URL , replace with the `CLIENT_ID` in the link: `https://discord.com/oauth2/authorize?scope=bot&permissions=0&client_id=CLIENT_ID`

## Elasticsearch

I created role with `view_index_metadata` and `create` and assigned it to my user.

To store, create an index, elastic sometimes doesn't want to understand datetime/epoch, so you might wanna use the below as mapping, I do it in the dev_tools/console:

```json
PUT /<discord_log_index>/_mapping
{
  "properties" : {
    "text": {
      "type": "text",
      "fields": {
        "keyword_type": {
        "type": "keyword"
        }
      }
    },
    "ts": {
      "type":"date",
      "format": "epoch_second"
    }
  }
}
```

## Ansible playbook

I have included a [provision-discord2elastic](provision-discord2elastic.yml) playbook you can use. Just change the "hosts" parameter and set some defaults in host/group_vars and you should be good to go:

host_vars/<docker_host>.yml:

```yml
discord2elastic_bot_token: sometoken
discord2elastic_elasticsearch_url: https://username:password@moose:9200/
discord2elastic_elasticsearch_index: discord_log
```

`ansible-provision provision-discord2elastic.yml`

## Build your own docker container

`export VERSION=(develop|vX.X.X)`

`make`

To run your own build: `make run`.

Modify the files as you see fit. You can upload new builds to your own repository with `make push`.
