sudo apt update
sudo apt install -y build-essential libssl-dev

wget https://security.appspot.com/downloads/vsftpd-2.3.4.tar.gz

tar xzf vsftpd-2.3.4.tar.gz
cd vsftpd-2.3.4

LINK -lcrypt

make 

sudo cp vsftpd /usr/local/sbin/

sudo mkdir /etc/vsftpd
sudo nano /etc/vsftpd/vsftpd.conf

listen=YES
anonymous_enable=YES
local_enable=YES
write_enable=YES
dirmessage_enable=YES
xferlog_enable=YES
connect_from_port_20=YES
chown_uploads=YES
chown_username=ftp
xferlog_std_format=YES
ftpd_banner=Welcome to vulnerable vsftpd server!

sudo /usr/local/sbin/vsftpd /etc/vsftpd/vsftpd.conf
