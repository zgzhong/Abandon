#ifndef SOCKET_PROJECT_PEER_H
#define SOCKET_PROJECT_PEER_H

#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>

#include <string>
#include <cstring>

// declaration of Peer
class Peer;

// declaration of TCP classes
class TCPPeer;
class TCPServer;
class TCPClntPeer;
class TCPSvrPeer;

// declaration of UDP classes
class UDPPeer;
class UDPClient;
class UDPServer;

// TCP utility function declaration
void writeMsg(const TCPPeer &, const std::string &);
void writeBlob(const TCPPeer &, const void *, const size_t &);
std::string readMsg(const TCPPeer &);
void *readBlob(const TCPPeer &);

// UDP utility function declaration



class Peer {
public:
    int m_sock;
    sockaddr_in m_address;

public:
    Peer() = default;

    Peer(const int &sock, const sockaddr_in &addr) : m_sock(sock), m_address() {
        std::memmove(&m_address, &addr, sizeof(addr));
    }

    Peer(const std::string &ip, const uint16_t &port) : m_sock(0), m_address() {
        std::memset(&m_address, 0, sizeof(m_address));

        m_address.sin_family = AF_INET;
        m_address.sin_port = htons(port);
        inet_pton(AF_INET, ip.c_str(), &m_address.sin_addr);
    }

    uint16_t getPort() const{
        return ntohs(m_address.sin_port);
    }
    std::string getIp() const {
        char ip[20];
        inet_ntop(AF_INET, &m_address.sin_addr, ip, INET_ADDRSTRLEN);
        return ip;
    }
};


/* ****************TCP Peers**************** */
class TCPPeer : public Peer {
public:
    friend void writeMsg(const TCPPeer &, const std::string &);
    friend void writeBlob(const TCPPeer &, const void *, const size_t &);
    friend std::string readMsg(const TCPPeer &);
    friend void *readBlob(const TCPPeer &);

    TCPPeer(const int &sock, const sockaddr_in &addr) : Peer(sock, addr) {}

    TCPPeer(const std::string ip, const uint16_t &port) : Peer(ip, port) {
        m_sock = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
    }

    const TCPPeer &shutdown() const { ::shutdown(m_sock, SHUT_RDWR); return *this;}
};

class TCPServer : public TCPPeer {
public:
    TCPServer(const std::string &ip, const uint16_t &port) : TCPPeer(ip, port) {}

    const TCPServer &bind() const;

    const TCPServer &listen(const int &backlog = 5) const;

    TCPClntPeer getClientPeer();  // get the connection from client
};

class TCPClntPeer : public TCPPeer {
public:
    TCPClntPeer(const std::string &ip, const uint16_t &port) : TCPPeer(ip, port) {}

    TCPClntPeer(const int &sock, const sockaddr_in &addr) : TCPPeer(sock, addr) {}
};

class TCPSvrPeer : public TCPPeer {
public:
    TCPSvrPeer(const std::string &ip, const uint16_t &port) : TCPPeer(ip, port) {}

    TCPSvrPeer& connect();
};


/* ****************UDP Peers**************** */
class UDPPeer : public Peer {
public:
    UDPPeer(const int &sock, const sockaddr_in &addr) : Peer(sock, addr) {
        m_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    }

    UDPPeer(const std::string &ip, const uint16_t &port) : Peer(ip, port) {
        m_sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    }

    void* Recvfrom(Peer&);

    void Sendto(const Peer& peer, const void* buf, const size_t &len);
};

class UDPServer : public UDPPeer {
public:
    UDPServer(const int &sock, const sockaddr_in &addr) : UDPPeer(sock, addr) {}

    UDPServer(const std::string &ip, const uint16_t &port) : UDPPeer(ip, port) {}

    UDPServer& bind();
};

class UDPClient : public UDPPeer {
public:
    UDPClient(const int &sock, const sockaddr_in &addr) : UDPPeer(sock, addr) {}

    UDPClient(const std::string &ip, const uint16_t &port) : UDPPeer(ip, port) {}
};

#endif //SOCKET_PROJECT_PEER_H
