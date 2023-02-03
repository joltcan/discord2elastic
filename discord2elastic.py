#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) 2023, Fredrik Lundhag <f@mekk.com>
# GNU General Public License v3.0+ (see https://www.gnu.org/licenses/gpl-3.0.txt)

from elasticsearch import Elasticsearch
import discord
import json
import time
import sys
import os

import logging

_log = logging.getLogger(__name__)

# Set environment variables
bot_token = os.getenv('BOT_TOKEN')
if not bot_token:
    print("Error: Please set BOT_TOKEN")
    print("export BOT_TOKEN=<somestring>")
    sys.exit(1)

elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
if not elasticsearch_url:
    print("Error: Please set ELASTICSEARCH_URL")
    print("export ELASTICSEARCH_URL=https://user:password@<somehost>:<port>")
    print("Note: port is mandatory due to the elastic implementation.")
    sys.exit(1)

elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
if not elasticsearch_index:
    print("Error: Please set ELASTICSEARCH_INDEX")
    print("export ELASTICSEARCH_INDEX=discord_log")
    sys.exit(1)

# connect to elastic
es = Elasticsearch(elasticsearch_url)

# create index
if not es.indices.exists(index = elasticsearch_index):
    try:
        es.indices.create(index = elasticsearch_index)
    except Exception as e:
        print("Error: couldn't create index: %s" % e)
        print("Bailing out")
        sys.exit(1)

if es:
    print("Connected to elasticsearch")

# connect to Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(m):
    doc = {}
    if m.author == client.user:
        return

    print(m)

    doc = {
        "channel": m.channel.name,
        "nick.name": m.author.nick,
        "team_id": "%s" % m.guild.id,
        "text": m.content,
        "type": m.type[0],
        "ts": "%s" % time.mktime(m.created_at.timetuple()),
        "user": m.author.name + '#' + m.author.discriminator,
        "user_team": m.guild.name,
    }

    # if a bot write there might not be a real nick
    if m.author.bot:
        doc['is_bot'] = True

    if nick.name:
        doc["nick.name"] = m.author.nick,
    else:
        doc["nick.name"] = m.author.name

    if nick.id:
        doc["nick.id"] = "%s" % m.author.id,

    if m.attachments:
        attachments = ""
        for a in m.attachments:
            attachments += "\nAttachment %s: [%s](%s)" %(a.id, a.filename, a.url)

        if doc['text']:
            doc['text'] += attachments
        else:
            doc['text'] = attachments

    if m.edited_at:
        doc["edited.ts"] = time.mktime(m.edited_at.timetuple())

    # wanna see how it looks?
    # print(json.dumps(doc, indent=1))

    res = es.index(index=elasticsearch_index, document=doc)

client.run(bot_token)