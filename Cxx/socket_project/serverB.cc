#include <iostream>
#include <fstream>
#include <cstdlib>
#include <string>
#include <utility>

#include "global.h"
#include "peer.h"
#include "server_util.h"



int main(){
    std::ifstream input("backendB.txt");
    dict_t dict = std::move(load_db(input));
    input.close(); // close the file

    UDPServer server = UDPServer("127.0.0.1", PORT_SERVER_B).bind();
    std::cout << "The Server B is up and running using UDP on port " << server.getPort() << "." << std::endl;

    // server loop
    while(1) {
        Peer peer;
        void *p = server.Recvfrom(peer);

        Query *query = (Query *) p;
        std::cout << "The Server B received input <" << query->m_input
                  <<"> and operation <" << query->get_fun() << ">" << std::endl;

        std::string result;
        int match_cnt=0, similar_cnt=0;
        switch(query->m_type){
            case search: {
                result = search_query(dict, query->m_input, match_cnt, similar_cnt);
                std::cout << "The Server B has found < " <<  match_cnt
                          << " > matches and < " << similar_cnt
                          << " > similar words" <<std::endl;
                break;
            }
            case prefix: {
                result = prefix_query(dict, query->m_input, match_cnt);
                std::cout << "The Server B has found < " << match_cnt << " > matches" << std::endl;
                break;
            }
            case suffix: {
                result = suffix_query(dict, query->m_input, match_cnt);
                std::cout << "The Server B has found < " << match_cnt << " > matches" << std::endl;
                break;
            }
            default:
                break;
        }

//        std::clog <<"Server-B: " << result << std::endl;
        server.Sendto(peer, result.c_str(), result.length() + 1);
        std::free(p);

        std::cout << "The Server B finished sending the output to AWS" << std::endl;
    }

    return EXIT_SUCCESS;
}