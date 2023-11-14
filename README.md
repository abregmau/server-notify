# server-notify

Simple server script for ubuntu that allows notifications to Telegram

Service:

Register our service in systemd and start it with the following commands::
sudo systemctl enable server-notify.service
sudo systemctl start server-notify.service

To check the status and restart the service after making a code update, we will use:
sudo systemctl status server-notify.service
sudo systemctl restart server-notify.service

Reference Link: https://medium.com/@crvc1998/bot-de-telegram-para-interactuar-con-servidor-linux-centos-7-e0857fa824b7
