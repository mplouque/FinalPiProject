nc -z -v 192.168.2.3 1-9999 > asdf.txt 2>&1; cat asdf.txt | grep 'succeeded'
