#include <sys/socket.h>
#include <iostream>
#include <string>
#include "peer.h"
#include "global.h"


// friend function
void writeMsg(const TCPPeer &peer, const std::string &msg){
    writeBlob(peer, msg.c_str(), msg.length()+1);
}

void writeBlob(const TCPPeer &peer, const void *p_blob, const size_t &len_blob ){
    write(peer.m_sock, &len_blob, sizeof(len_blob));
    write(peer.m_sock, p_blob, len_blob);
}

std::string readMsg(const TCPPeer &peer){
    const char* msg = (char *)readBlob(peer);
    std::string msg_str(msg);
    delete []msg;
    return msg_str;
}

void* readBlob(const TCPPeer &peer){
    size_t blob_len = 0;
    read(peer.m_sock, &blob_len, sizeof(blob_len));

    auto *buf = new char[blob_len];
    read(peer.m_sock, buf, blob_len);

    return buf;
}



// TCP Server
const TCPServer& TCPServer::bind() const{
    int stat = ::bind(m_sock, (SA *)&m_address, sizeof(m_address));

    if (stat < 0){
        std::cerr << "bind error" << std::endl;
    }
    return *this;
}

const TCPServer& TCPServer::listen(const int &backlog) const{
    int stat = ::listen(m_sock, backlog);

    if (stat < 0){
        std::cerr << "Listen error" << std::endl;
    }

    return *this;
}

TCPClntPeer TCPServer::getClientPeer() {
    int clnt_sock = 0;
    sockaddr_in clnt_addr;
    socklen_t  addr_len;
    clnt_sock = accept(m_sock, (SA*)&clnt_addr, &addr_len);

    TCPClntPeer clientPeer(clnt_sock, clnt_addr);
    return clientPeer;
}


// TCPSvrPeer
TCPSvrPeer& TCPSvrPeer::connect() {
    ::connect(m_sock, (SA*)&m_address, sizeof(m_address));

    return *this;
}


// UDPPeer
void* UDPPeer::Recvfrom(Peer &peer) {
    void *buf = std::malloc((MAX_LINE+1)*sizeof(char));

    std::memset(buf, 0, MAX_LINE+1);
    socklen_t  addr_len = sizeof(peer.m_address);
    ssize_t len = recvfrom(this->m_sock, buf, MAX_LINE, 0, (SA*)&(peer.m_address), &addr_len);

    return buf;
}


void UDPPeer::Sendto(const Peer &peer, const void* buf, const size_t &len) {
    sendto(this->m_sock, buf, len, 0, (SA*)&(peer.m_address), sizeof(peer.m_address));
}


// UDPServer
UDPServer& UDPServer::bind() {
    int stat = ::bind(m_sock, (SA*)&m_address, sizeof(m_address));

    if (stat < 0){
        std::cerr << "UDP: sock bind address failed" << std::endl;
    }

    return *this;
}
