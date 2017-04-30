import os, sys, logging
import re
import time
from slackclient import SlackClient
from dxlclient.client import DxlClient
from dxlclient.client_config import DxlClientConfig
from dxlclient.message import Message, Request

#from dxlmarclient import MarClient

#from dxlepoclient import EpoClient, OutputFormat

from dxltieclient import TieClient
from dxltieclient.constants import HashType, TrustLevel, FileProvider, ReputationProp, CertProvider, CertReputationProp, CertReputationOverriddenProp

# Import common logging and configuration
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/..")
#from common import *

# Enable logging, this will also direct built-in DXL log messages.
# See - https://docs.python.org/2/howto/logging-cookbook.html
log_formatter = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

## DXL Client Configuration
CONFIG_FILE_NAME = "/vagrant/dxlclient.config"

# Create DXL configuration from file
config = DxlClientConfig.create_dxl_config_from_file(CONFIG_FILE_NAME)
CONFIG_FILE = os.path.dirname(os.path.abspath(__file__)) + "/" + CONFIG_FILE_NAME

# instantiate Slack & Twilio clients
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))

## Check if it is a SHA1
def is_sha1(maybe_sha):
    if len(maybe_sha) != 40:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is a SHA256
def is_sha256(maybe_sha):
    if len(maybe_sha) != 64:
        return False
    try:
        sha_int = int(maybe_sha, 16)
    except ValueError:
        return False
    return True

## Check if it is an MD5
def is_md5(maybe_md5):
    if len(maybe_md5) != 32:
        return False
    try:
        md5_int = int(maybe_md5, 16)
    except ValueError:
        return False
    return True

## TIE Reputation Average Map
tiescoreMap = {0:'Not Set', 1:'Known Malicious', 15: 'Most Likely Malicious', 30: 'Might Be Malicious',50: 'Unknown',70:"Might Be Trusted",85: "Most Likely Trusted", 99: "Known Trusted",100: "Known Trusted Installer"}
## TIE Provider Map
providerMap = {1:'GTI', 3:'Enterprise Reputation', 5:'ATD',7:"MWG"}

## Get File Properties and Map with Providers and TIE Score
def getFileProps(myReturnVal):
    fileProps = myReturnVal
    propList = []

    if FileProvider.GTI in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.GTI]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.GTI]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.GTI]['createDate']
        propList.append(propDict)

    if FileProvider.ENTERPRISE in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.ENTERPRISE]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.ENTERPRISE]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.ENTERPRISE]['createDate']
        propList.append(propDict)

    if FileProvider.ATD in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.ATD]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.ATD]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.ATD]['createDate']
        propList.append(propDict)

    if FileProvider.MWG in fileProps:
        propDict = {}
        propDict['provider'] = providerMap[fileProps[FileProvider.MWG]['providerId']]
        propDict['reputation'] = tiescoreMap[fileProps[FileProvider.MWG]['trustLevel']]
        propDict['createDate'] = fileProps[FileProvider.MWG]['createDate']
        propList.append(propDict)

    return propList

## Get the file reputation properties from TIE using md5 or sha1
def getTieRep(md5,sha1,sha256):
    with DxlClient(config) as client:
        # Connect to the fabric
        client.connect()

        # Create the McAfee Threat Intelligence Exchange (TIE) client
        tie_client = TieClient(client)

        #
        # Request and display reputation for notepad.exe
        #
        if md5:
            reputations_dict = tie_client.get_file_reputation({HashType.MD5: md5})
        if sha1:
            reputations_dict = tie_client.get_file_reputation({HashType.SHA1: sha1})
        if sha256:
            reputations_dict = tie_client.get_file_reputation({HashType.SHA256: sha256})

            #myReturnVal = json.dumps(reputations_dict, sort_keys=True, indent=4, separators=(',', ': ')) + "\n"
    return reputations_dict

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

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(EXAMPLE_COMMAND):
        response = "Sure...write some more code then I can do that!"
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def getFileRep(md5=None,sha1=None,sha256=None):
    if md5 == None and sha1 == None and sha256 == None:
        return "no file hash"
    else:
        ### Verify SHA1 string
        if sha1 != None:
            if not is_sha1(sha1):
                return "invalid sha1"

        ### Verify SHA256 string
        if sha256 != None:
            if not is_sha256(sha256):
                return "invalid sha256"

        if md5 != None:
            if not is_md5(md5):
                return "invalid md5"

        myReturnProps = getTieRep(md5,sha1,sha256)
        ### Load JSON into fileProps Dictionary
        propList = getFileProps(myReturnProps)

        return myReturnProps

def takeAction(commandStr,channel):
    checkTie = re.compile('check\s+md5\s+[a-f0-9]{32}\s*')
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
                slack_client.api_call("chat.postMessage", channel=channel,
                                  text=response, as_user=True)
                return True
    else:
        return False

if __name__ == "__main__":
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
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
                if takeAction(command,channel) == False:
                    handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
