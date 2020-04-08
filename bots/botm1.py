#!/usr/bin/env python3
# coding: utf-8

import os
import sys
from configparser import ConfigParser
from pyngrok import ngrok
import logging
import time
import json

filename = os.path.join(os.path.dirname(__file__), '..')
sys.path.insert(1, filename)
from zoomapi import OAuthZoomClient

# Get config
logging.basicConfig(level=logging.INFO)
config_file = "bots/bot.ini"
parser = ConfigParser()
parser.read(config_file)
client_id = parser.get("OAuth", "client_id")
client_secret = parser.get("OAuth", "client_secret")
port = parser.getint("OAuth", "port", fallback=4001)
browser_path = parser.get("OAuth", "browser_path")

# Create http server
redirect_url = ngrok.connect(port, "http")

# Create Zoom client
client = OAuthZoomClient(client_id, client_secret, port, redirect_url, browser_path)

# Test chat_channels
# list
logging.info("=====================================================")
logging.info("Test chat_channels, list")
response = client.chat_channels.list()
assert response.status_code == 200
time.sleep(2)
logging.info("Number of channels: {}".format(len(json.loads(response.content)["channels"])))

# create
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, create")
new_channel_name = "new_channel"
response = client.chat_channels.create(name=new_channel_name, type=1, members=[])
assert response.status_code == 200
print(response.content)
time.sleep(2)
logging.info("Number of channels: {}".format(len(json.loads(client.chat_channels.list().content)["channels"])))
new_channel_id = json.loads(response.content)["id"]
logging.info("Create new channel, new channel id : {}".format(new_channel_id))

# get
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, get")
logging.info("Get channel with id : {}".format(new_channel_id))
response = client.chat_channels.get(channelId=new_channel_id)
logging.info(json.loads(response.content))
assert response.status_code == 200

# update
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, update")
logging.info("Update channel with id : {}".format(new_channel_id))
response = client.chat_channels.update(channelId=new_channel_id, name="change_new_channel")
assert response.status_code == 204

# list members
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, list members")
logging.info("List members in channel {}".format(new_channel_id))
response = client.chat_channels.list_members(channelId=new_channel_id)
logging.info(json.loads(response.content))
assert response.status_code == 200

# invite members
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, invite members")
member = "zihuaw2@uci.edu"
logging.info("Invite {} to channel {}".format(member, new_channel_id))
members_to_invite = [{"email": member}]
response = client.chat_channels.invite_member(channelId=new_channel_id, members=members_to_invite)
logging.info(json.loads(response.content))
assert response.status_code == 200

# delete
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, delete")
logging.info("Delete channel with id : {}".format(new_channel_id))
response = client.chat_channels.delete(channelId=new_channel_id)
assert response.status_code == 204

# leave
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, leave")
# first create one new channel and leave
test_leave_new_channel_name = "test_leave"
test_leave_new_channel_id = \
    json.loads(client.chat_channels.create(name=test_leave_new_channel_name, type=1, members=[]).content)["id"]
time.sleep(2)
logging.info("Create new channel with id : {} and leave".format(test_leave_new_channel_id))
response = client.chat_channels.leave(channelId=test_leave_new_channel_id)
assert response.status_code == 204

# join
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, join")
test_join_leave_channel_id = "24697ebe-a7cf-423e-89fd-a9bb9873e036"
logging.info("Join channel with id : {}".format(test_join_leave_channel_id))
for channel in json.loads(client.chat_channels.list().content)["channels"]:
    if channel["id"] == test_join_leave_channel_id:
        time.sleep(2)
        response = client.chat_channels.leave(channelId=test_join_leave_channel_id)
        assert response.status_code == 204
time.sleep(2)
response = client.chat_channels.join(channelId=test_join_leave_channel_id)
logging.info(json.loads(response.content))
assert response.status_code == 200
time.sleep(2)
response = client.chat_channels.leave(channelId=test_join_leave_channel_id)
assert response.status_code == 204

# remove member
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_channels, remove")
# first create one new channel and remove me
test_remove_member_new_channel_name = "test_remove_member"
test_remove_member_new_channel_id = \
    json.loads(client.chat_channels.create(name=test_remove_member_new_channel_name, type=1, members=[]).content)["id"]
time.sleep(2)
logging.info('Create new channel with id : {} and remove member "me"'.format(test_remove_member_new_channel_id))
response = client.chat_channels.remove_member(channelId=test_remove_member_new_channel_id, memberId="me")
assert response.status_code == 204

# Test chat_message
# list
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_message, list")
to_contact = "zihuaw2@uci.edu"
logging.info("List all messages in chat channel with {}".format(to_contact))
response = client.chat_messages.list(userId="me", to_contact=to_contact)
logging.info(json.loads(response.content))
assert response.status_code == 200

# send
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_message, send")
message_to_send = "Nice to meet you!"
logging.info("Send message {} to {}".format(message_to_send, to_contact))
response = client.chat_messages.send(message=message_to_send, to_contact=to_contact)
logging.info(json.loads(response.content))
assert response.status_code == 201
message_id = json.loads(response.content)["id"]

# update
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_message, update")
message_to_send = "(Edited) Nice to meet you again!"
logging.info("Update sent messages to {}".format(message_to_send))
response = client.chat_messages.update(messageId=message_id, message=message_to_send, to_contact=to_contact)
assert response.status_code == 204

# delete
time.sleep(2)
logging.info("=====================================================")
logging.info("Test chat_message, delete")
logging.info("Delete message just sent")
response = client.chat_messages.delete(messageId=message_id, to_contact=to_contact)
assert response.status_code == 204
