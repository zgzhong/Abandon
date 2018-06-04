CC = g++
CFLAGS = -O2 -std=c++11

all: client.cc monitor.cc aws.cc serverA.cc serverB.cc serverC.cc peer.cc
	$(CC) $(CFLAGS) client.cc peer.cc -o client
	$(CC) $(CFLAGS) monitor.cc peer.cc -o monitor
	$(CC) $(CFLAGS) aws.cc peer.cc -o aws
	$(CC) $(CFLAGS) serverA.cc peer.cc -o serverA
	$(CC) $(CFLAGS) serverB.cc peer.cc -o serverB
	$(CC) $(CFLAGS) serverC.cc peer.cc -o serverC

.PHONY: clean monitor aws serverA serverB serverC

monitor:
	./monitor
aws:
	./aws
serverA: backendA.txt 
	./serverA
serverB: backendB.txt
	./serverB
serverC: backendC.txt
	./serverC
clean:
	rm client monitor aws serverA serverB serverC
