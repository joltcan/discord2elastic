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
    print("Error: Please set BOT_TOKEN", flush=True)
    print("export BOT_TOKEN=<somestring>", flush=True)
    sys.exit(1)

elasticsearch_url = os.getenv('ELASTICSEARCH_URL')
if not elasticsearch_url:
    print("Error: Please set ELASTICSEARCH_URL", flush=True)
    print("export ELASTICSEARCH_URL=https://user:password@<somehost>:<port>", flush=True)
    print("Note: port is mandatory due to the elastic implementation.", flush=True)
    sys.exit(1)

elasticsearch_index = os.getenv('ELASTICSEARCH_INDEX')
if not elasticsearch_index:
    print("Error: Please set ELASTICSEARCH_INDEX", flush=True)
    print("export ELASTICSEARCH_INDEX=discord_log", flush=True)
    time.sleep(5)
    sys.exit(1)

# set if more info is needed
debugprint = os.getenv('DEBUG')

# connect to elastic
es = Elasticsearch(elasticsearch_url)

# create index
if not es.indices.exists(index = elasticsearch_index):
    try:
        es.indices.create(index = elasticsearch_index)
    except elasticsearch.AuthorizationException as e:
        print("Error: couldn't create index: %s" % e, flush=True)
        print("Bailing out", flush=True)
        s
        sys.exit(1)

if es:
    print("Connected to elasticsearch", flush=True)

# connect to Discord
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}', flush= True)

@client.event
async def on_message(m):
    doc = {}
    if m.author == client.user:
        return

    # debug output of the whole message type
    if debugprint:
        print(m, flush=True)

    # create basic message structure
    doc = {
        "channel": m.channel.name,
        "team_id": str(m.guild.id),
        "text": m.content,
        "type": str(m.type[0]),
        "ts": time.mktime(m.created_at.timetuple()),
        "user": m.author.name + '#' + str(m.author.discriminator),
        "user_team": str(m.guild.name),
    }

    # if a bot write there might not be a real nick
    if m.author.bot:
        doc['is_bot'] = m.author.bot

    # use author nick, but use name if it's from a bot since they don't have a nick
    try:
        doc["nick.name"] = m.author.nick
    except:
        doc["nick.name"] = m.author.name

    # convert to string
    if m.author.id:
        doc["nick.id"] = str(m.author.id),

    # append a list of attachments if someone wanna build a ui at some pount.
    if m.attachments:
        attachments = ""
        for a in m.attachments:
            attachments += "\nAttachment %s: [%s](%s)" %(a.id, a.filename, a.url)

        doc['text'] += attachments

    if m.edited_at:
        doc["edited.ts"] = time.mktime(m.edited_at.timetuple())

    if debugprint:
        print(json.dumps(doc, indent=1), flush=True)

    try:
        res = es.index(index=elasticsearch_index, document=doc)
    except ElasticsearchWarning as e:
        print("Warning from elastic: %s" % e, flush=True)

    if debugprint:
        print(res, flush=True)

client.run(bot_token)
