// system header
#include <netinet/in.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>

// cpp header
#include <iostream>
#include <ostream>
#include <string>
#include <cstring>
#include <vector>

// project header
#include "global.h"
#include "peer.h"
#include "aws.h"

std::ostream& print_clnt_msg(const Query *p, const Peer &peer ,std::ostream &os);
std::ostream& print_back_msg(const Result &result, const Peer &peer, const Query & query, std::ostream&);


int main(int argc, char* argv[]){
    TCPServer awsQuery = TCPServer("127.0.0.1", PORT_AWS_CLNT).bind().listen();
    TCPServer awsMonitor = TCPServer("127.0.0.1", PORT_AWS_MONITOR).bind().listen();
    UDPServer awsUDP = UDPServer("127.0.0.1", PORT_AWS_UDP).bind();
    UDPClient serverA("127.0.0.1", PORT_SERVER_A);
    UDPClient serverB("127.0.0.1", PORT_SERVER_B);
    UDPClient serverC("127.0.0.1", PORT_SERVER_C);
    std::cout << "The AWS is up and running" << std::endl;

     TCPClntPeer monitorPeer = awsMonitor.getClientPeer();  // establish the connection with monitor

    while (1) {
        // get query from client
        TCPClntPeer clntPeer = awsQuery.getClientPeer();
        auto *p_query = (Query *) readBlob(clntPeer);
        print_clnt_msg(p_query, clntPeer, std::cout) << std::endl;

        // send query to backend server
        awsUDP.Sendto(serverA, p_query, sizeof(Query));
        std::cout << "The AWS sent <" << p_query->m_input <<"> and <" << p_query->get_fun() << "> to Backend-Server A." << std::endl;
        awsUDP.Sendto(serverB, p_query, sizeof(Query));
        std::cout << "The AWS sent <" << p_query->m_input <<"> and <" << p_query->get_fun() << "> to Backend-Server B." << std::endl;
        awsUDP.Sendto(serverC, p_query, sizeof(Query));
        std::cout << "The AWS sent <" << p_query->m_input <<"> and <" << p_query->get_fun() << "> to Backend-Server C." << std::endl;

        // receive result from backend server
        Peer peer1, peer2, peer3;
        void *p1 = awsUDP.Recvfrom(peer1);
        Result ret1 = Result(p1, p_query);
        print_back_msg(ret1, peer1, *p_query, std::cout) << std::endl;
        void *p2 = awsUDP.Recvfrom(peer2);
        Result ret2 = Result(p2, p_query);
        print_back_msg(ret2, peer2, *p_query, std::cout) << std::endl;
        void *p3 = awsUDP.Recvfrom(peer3);
        Result ret3 = Result(p3, p_query);
        print_back_msg(ret3, peer3, *p_query, std::cout) << std::endl;

        Result results = Result({ret1, ret2, ret3});

        std::free(p1);
        std::free(p2);
        std::free(p3);

        writeMsg(clntPeer, results.to_client());
        std::cout << "The AWS sent <" <<results.get_match_cnt() << "> matches to client." << std::endl;
        writeMsg(monitorPeer, results.to_monitor());
        if (p_query->m_type == search) {
            if(results.get_match_cnt()) {
                std::cout << "The AWS sent < " << p_query->m_input
                          << "> and <" << results.similar_word()
                          << "> to the monitor via TCP port " << PORT_AWS_MONITOR
                          << " for " << p_query->get_fun()
                          << std::endl;
            }
            else{
                std::cout << "The AWS sent no match found to the monitor via TCP port" << PORT_AWS_MONITOR
                          << " for " << p_query->get_fun() << std::endl;

            }
        }
        else{
            std::cout << "The AWS sent <" << results.get_match_cnt()
                      << "> matches to the monitor via TCP port <" << PORT_AWS_MONITOR
                      << "> for "<< p_query->get_fun() << std::endl;
        }
        delete p_query;
        clntPeer.shutdown();
    }

    return 0;
}


std::ostream& print_clnt_msg(const Query *p, const Peer &peer ,std::ostream &os){
    os << "The AWS received input=<" << p->m_input
       << "> and function=<" << p->get_fun()
       << "> from client using TCP over port " << peer.getPort();

    return os;
}

std::ostream& print_back_msg(const Result &result, const Peer &peer, const Query &query, std::ostream &os ){
    os << "The AWS received";
    if(query.m_type == search){
        os << " <" << result.get_similar_cnt() << "> ";
    }
    else{
        os << " <" << result.get_match_cnt() << "> ";
    }

    os << "from Backend-Server ";
    if (peer.getPort() == PORT_SERVER_A)
        os << "A ";
    else if(peer.getPort() == PORT_SERVER_B)
        os << "B ";
    else
        os << "C ";
    os << "using UDP over port " << peer.getPort();
    return os;
}
