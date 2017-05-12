# This sample demonstrates how to register a DXL service to receive Request
# messages and send Response messages back to an invoking client.

import logging
import os
import sys
import time,json
from base64 import *
from slackclient import SlackClient

from dxlclient.callbacks import EventCallback
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig

from dxltieclient import TieClient
from dxltieclient.constants import HashType, TrustLevel, FileProvider, ReputationProp, CertProvider, CertReputationProp, CertReputationOverriddenProp


# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/.")
from common import *

# Configure local logger
logging.getLogger().setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

# Topic used to notify that a file reputation has changed
TIE_EVENT_FILE_REPUTATION_CHANGE_TOPIC = "/mcafee/event/tie/file/repchange/broadcast"

# Topic used to notify that a file detection has occurred
TIE_EVENT_FILE_DETECTION_TOPIC = "/mcafee/event/tie/file/detection"

TIE_FILE_REPUTATION_UPDATE = "/mcafee/service/tie/reputation/updates"

TIE_FILE_REPUTATION = "/mcafee/service/tie/file/reputation"

# Topic used to notify when the first instance of a file has been found
TIE_EVENT_FILE_FIRST_INSTANCE_TOPIC = "/mcafee/event/tie/file/firstinstance"

TIE_META = "/mcafee/service/tie/file/update_metadata"

# The topic for the service to respond to
#SERVICE_TOPIC = "/scottbrumley/sample/basicevent"

## DXL Client Configuration
CONFIG_FILE_NAME = "/vagrant/dxlclient.config"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE_NAME)
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/" + CONFIG_FILE_NAME

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

## TIE Reputation Average Map
tiescoreMap = {0:'Not Set', 1:'Known Malicious', 15: 'Most Likely Malicious', 30: 'Might Be Malicious',50: 'Unknown',70:"Might Be Trusted",85: "Most Likely Trusted", 99: "Known Trusted",100: "Known Trusted Installer"}
## TIE Provider Map
providerMap = {1:'GTI', 3:'Enterprise Reputation', 5:'ATD',7:"MWG"}

def get_bot_id():
    '''
    Use the environment variable BOT_NAME to get the BOT ID from 
    Slack and returns the BOT ID
    '''
    BOT_NAME = os.environ.get('BOT_NAME')
    api_call = slack_client.api_call("users.list")
    if api_call.get('ok'):
        # retrieve all users so we can find our bot
        users = api_call.get('members')
        for user in users:
            if 'name' in user and user.get('name') == BOT_NAME:
                return user.get('id')

    else:
        print("could not find bot user with the name " + BOT_NAME)

def takeAction(commandStr,channel):
    checkTie = re.compile('check\s+md5\s+[a-f0-9]{32}\s*')
    slackResponse = ""
    print commandStr
    if checkTie.match(commandStr):
        response = "Looking up md5 hash ..."
        slack_client.api_call("chat.postMessage", channel=channel,
                              text=response, as_user=True)
        md5 = re.search('check\s+md5\s+([a-f0-9]{32})', commandStr)
        if md5:
            myHash = md5.group(1)
            if is_md5(myHash):
                response = getFileRep(myHash)
                content = getFileProps(response)

                slackResponse = "File Hash *" + myHash + "* Reputation\n"
                ## Format a Slack Response
                i = 1
                for key in content:
                    slackResponse = slackResponse + "*Provider: " + key['provider'] + "*\n"
                    slackResponse = slackResponse + "Creation Date: " + convertEpoc(key['createDate']) + "\n"
                    slackResponse = slackResponse + "Reputation: " + key['reputation'] + "\n"
                    slackResponse = slackResponse + "\n"
                    i = i + 1

                slack_client.api_call("chat.postMessage", channel=channel,
                                      text=slackResponse, as_user=True)
                return True
    else:
        return False

# Create the client
with DxlClient(config) as client:
    # Connect to the fabric
    client.connect()
    class ChgRepCallback(EventCallback):
        def on_event(self, event):
            slackMsg = ""
            # Extract
            slackMsg = slackMsg + "*Changed Reputation received:* \n"
            resultStr = json.loads(event.payload.decode())
            slackMsg = slackMsg + "*Hashes:* " + "\n"

            ## Print Hashes
            retHashes = resultStr['hashes']
            for hash in retHashes:
                slackMsg = slackMsg + "*Hash Type:* " + hash['type'] + "\n *Hash Value:* " + b64decode(hash['value']).encode("hex") + "\n"

            ## Print Old Reps
            slackMsg = slackMsg + "\n*Old Reputation:*\n"
            for vals in resultStr['oldReputations']['reputations']:
                slackMsg = slackMsg + "*Provider:* " + providerMap[vals['providerId']] + "\n"
                slackMsg = slackMsg + "*Creation Date:* " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vals['createDate'])) + "\n"
                slackMsg = slackMsg + "*Reputation Score:* " +  tiescoreMap[vals['trustLevel']] + "\n"

            ## Print New Reps
            slackMsg = slackMsg + "\n*New Reputation:*\n"
            for vals in resultStr['newReputations']['reputations']:
                slackMsg = slackMsg + "*Provider:* " + providerMap[vals['providerId']] + "\n"
                slackMsg = slackMsg + "*Date:* " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vals['createDate'])) + "\n"
                slackMsg = slackMsg + "*Reputation Score:* " +  tiescoreMap[vals['trustLevel']] + "\n"

            slack_client.api_call(
                "chat.postMessage",
                channel="#security",
                text=slackMsg,
                as_user=True
            )

    class NewRepCallback(EventCallback):
        def on_event(self, event):
            # Extract
            print "New Reputation received: " + event.payload.decode()
            resultStr = json.loads(event.payload.decode())
            print "Hashes: "

            print resultStr

            ## Print Hashes
            retHashes = resultStr['hashes']
            for hash in retHashes:
                print hash['type'] + " " + b64decode(hash['value']).encode("hex")

            ## Print Old Reps
            print "Old Reputations:"
            for vals in resultStr['oldReputations']['reputations']:
                print providerMap[vals['providerId']]
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vals['createDate']))
                print tiescoreMap[vals['trustLevel']]

            ## Print New Reps
            print "New Reputations:"
            for vals in resultStr['newReputations']['reputations']:
                print providerMap[vals['providerId']]
                print time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(vals['createDate']))
                print tiescoreMap[vals['trustLevel']]


    # starterbot's ID as an environment variable
    BOT_ID = get_bot_id()

    if BOT_ID == None:
        print "BOT_ID is missing from ENV"
        exit(0)

    # constants
    AT_BOT = "<@" + BOT_ID + ">"
    EXAMPLE_COMMAND = "do"

    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():

        client.add_event_callback(TIE_EVENT_FILE_REPUTATION_CHANGE_TOPIC, ChgRepCallback())
        client.add_event_callback(TIE_EVENT_FILE_FIRST_INSTANCE_TOPIC, NewRepCallback())

        time.sleep(READ_WEBSOCKET_DELAY)
        logger.info("Slack/TIE Listener is running ... ")
    else:
        print("Connection failed. Invalid Slack token or bot ID?")

    while True:
        time.sleep(60)

