CC = clang++
CFLAG = -Wall -O2 -std=c++11


all: rreadline

.SUFFIXES: .cpp .c

.cpp.o:
	$(CC) -c $(CFLAG) $<

rreadline: main.o rreadline.o
	$(CC) main.o rreadline.o  -o rreadline

.PHONY:clean

clean:
	rm *.o
