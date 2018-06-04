#include <unistd.h>

#include <iostream>
#include <string>
#include <cstring>

#include "global.h"
#include "peer.h"


int main(int argc, char* argv[]){
    if(argc != 3){
        std::cerr << "Usage: ./client <function> <m_input>" << std::endl;
        return EXIT_FAILURE;
    }
    std::string function(argv[1]);
    std::string input(argv[2]);

    Query q(function, input);
    TCPSvrPeer svrPeer("127.0.0.1", PORT_AWS_CLNT);

    // connect to server
    svrPeer.connect();
    std::clog << "The client is up and running." << std::endl;

    // send query to aws server
    writeBlob(svrPeer, &q, sizeof(q));
    std::clog << "The client sent < " << input
              << " > and < " << function
              << " > to AWS." << std::endl;

    auto result = readMsg(svrPeer);
    std::clog << result << std::endl;

    svrPeer.shutdown();
    return 0;
}

