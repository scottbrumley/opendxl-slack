# Requirements

### For Repo
* Put your broker certs in the brokercerts/ directory [Certificate Setup](./cert_setup.md)
* Put your client certificates in the certs/ directory [Certificate Setup](./cert_setup.md)
* Edit dxlclient.config and add your Broker(s)

### For Automated Environment
1. Download Vagrant https://www.vagrantup.com/downloads.html
2. Run installer for Vagrant
3. Download Virtualbox https://www.virtualbox.org/wiki/Downloads?replytocom=98578
4. Run installer for Virtualbox
3. Download Git https://git-scm.com/downloads

### Slack Environment Variables
* Create a file named scripts/env.sh
* Make executable chmod +x scripts/env.sh
```
#!/bin/bash
echo "export SLACK_BOT_TOKEN='MY BOT TOKEN'" | sudo tee -a /etc/environment
echo "export BOT_NAME='MY BOT NAME'" | sudo tee -a /etc/environment

```