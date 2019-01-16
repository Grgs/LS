#!/usr/bin/fish
chmod 700 ~/.ssh; and chmod 600 ~/.ssh/authorized_keys
service ssh --full-restart
#sudo service ssh start
ssh -i .ssh/ssh-ecdsa localhost -p "8822" -v

