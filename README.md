# discord2elastic aka log2elastic

Sometimes you want chatlogs to be searchable. Put them in elasticsearch and keep em!

## setup

discord2elastic runs by itself. Set the environment variables and go ahead. 

You first need a discord user, see the Discord topic for reference. 

You also need a elasticsearch user that can create indices and write them.

Run it manually or use the ansible playbook:

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

## Ansible

I have included a [provision-discord2elastic](provision-discord2elastic.yml) playbook you can use. Just change the "hosts" parameter and set some defaults in host/group_vars and you should be good to go:

host_vars/<docker_host>.yml:

```yml
discord2elastic_bot_token: sometoken
discord2elastic_elasticsearch_url: https://elastic:9200
discord2elastic_elasticsearch_index: discord_log
```

`ansible-provision provision-discord2elastic.yml`

## Build your own docker container

`export VERSION=(develop|vX.X.X)`

`make`

To run your own build: `make run`.

Modify the files as you see fit. You can upload new builds to your own repository with `make push`.
