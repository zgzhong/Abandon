#ifndef SOCKET_PROJECT_GLOBAL_H
#define SOCKET_PROJECT_GLOBAL_H

#include <cstdio>
#include <string>
#include <cstring>
#include <ostream>
#include <sstream>
#include <utility>
#include <sys/socket.h>


using SA = sockaddr; // c++11
const int MAX_LINE = 4096;

// all server port
const uint16_t PORT_BASE = 512;
const uint16_t PORT_SERVER_A    = 21000 + PORT_BASE;
const uint16_t PORT_SERVER_B    = 22000 + PORT_BASE;
const uint16_t PORT_SERVER_C    = 23000 + PORT_BASE;
const uint16_t PORT_AWS_UDP     = 24000 + PORT_BASE;
const uint16_t PORT_AWS_CLNT    = 25000 + PORT_BASE;
const uint16_t PORT_AWS_MONITOR = 26000 + PORT_BASE;

enum Fun{
    search,
    prefix,
    suffix
};

class Query{
public:
    Fun m_type;
    char m_input[28];

    Query(const std::string &func, const std::string& word){
        if (func == "prefix")
            m_type = prefix;
        else if (func == "suffix")
            m_type = suffix;
        else
            m_type = search;

        std::strcpy(m_input, word.c_str());
    }

    const std::string get_fun() const{
        switch (m_type){
            case search: return "search"; break;
            case prefix: return "prefix"; break;
            default: return "suffix"; break;
        }
    }
};


#endif //SOCKET_PROJECT_GLOBAL_H
