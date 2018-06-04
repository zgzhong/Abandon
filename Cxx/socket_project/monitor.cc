#include <iostream>
#include <string>

#include "global.h"
#include "peer.h"

int main(){
    TCPSvrPeer aws = TCPSvrPeer("127.0.0.1", PORT_AWS_MONITOR).connect();

    std::cout << "The monitor is up and running" << std::endl;
    while (1){
        auto msg = readMsg(aws);
        if (msg.length() == 0)
            break;
        std::cout << msg;
    }

    // close connection
     aws.shutdown();

    return 0;
}