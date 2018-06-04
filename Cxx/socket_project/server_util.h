#ifndef SOCKET_PROJECT_BACKEND_SERVER_H
#define SOCKET_PROJECT_BACKEND_SERVER_H

#include <map>
#include <set>
#include <vector>
#include <fstream>
#include <utility>
#include <cctype>

#include <istream>

using item_t = std::pair<std::string, std::string>;
using dict_t = std::multimap<std::string, std::string>;
using std::tolower;

// parse every read from file
item_t parse_line(std::string line) {
    const std::string delimiter = " :: ";
    size_t pos = 0;
    pos = line.find(delimiter);
    std::string key = line.substr(0, pos);
    line.erase(0, pos + delimiter.length());

    return {key, line};
}

// read dict file
dict_t load_db(std::istream &ifs) {
    std::string line;
    dict_t dict;

    while (std::getline(ifs, line)) {
        item_t kv = parse_line(line);
        dict.insert(kv);
    }

    return dict;
}

std::string search_query(const dict_t &dict, const std::string &word, int &match_cnt, int &similar_cnt) {
    std::ostringstream osstrm;
    std::vector<std::string> match_vec;
    std::vector<std::string> similar_word_vec;
    std::vector<std::string> similar_vec;

    for (auto map_it = dict.cbegin(); map_it != dict.cend(); ++map_it){
        auto key = map_it->first;
        if (key.length() == word.length()) {
            auto key_it = key.cbegin();
            int mis_match_cnt = 0;

            for(auto it=word.cbegin(); it!=word.cend(); ++it, ++key_it){
                if (tolower(*it) != tolower(*key_it))
                    ++mis_match_cnt;
            }

            if(mis_match_cnt == 0){
                match_vec.push_back(map_it->second);
            }
            if(mis_match_cnt == 1){
                similar_word_vec.push_back(map_it->first);
                similar_vec.push_back(map_it->second);
            }
        }
    }

    match_cnt = match_vec.size();
    similar_cnt = similar_vec.size();

    osstrm << match_cnt << std::endl;
    for(const auto&x: match_vec){
        osstrm << x << std::endl;
    }
    osstrm << similar_cnt << std::endl;
    auto word_it = similar_word_vec.cbegin();
    auto def_it = similar_vec.cbegin();
    for(int i =0; i< similar_cnt; ++i){
        osstrm << *word_it << std::endl;
        osstrm << *def_it << std::endl;

        ++word_it;
        ++def_it;
    }
    return osstrm.str();
}

std::string prefix_query(const dict_t &dict, const std::string &word, int &match_cnt) {
    std::ostringstream osstrm;
    std::set<std::string> word_set;

    for(auto map_it = dict.cbegin(); map_it != dict.cend(); ++map_it) {
        auto key = map_it->first;
        auto key_it = key.cbegin();
        bool is_prefix = true;
        for(auto it=word.cbegin(); it!= word.cend(); ++it, ++key_it){
            if(key_it == key.cend()  || tolower(*key_it) != tolower(*it)){
                is_prefix = false;
                break;
            }
        }
        if (is_prefix){
            word_set.insert(key);
        }
    }
    match_cnt = word_set.size();

    osstrm << word_set.size() << std::endl;
    for (const auto &x: word_set){
        osstrm << x << std::endl;
    }
    osstrm << 0 << std::endl;  // similar count
    return osstrm.str();
}

std::string suffix_query(const dict_t &dict, const std::string &word, int &match_cnt) {
    std::ostringstream osstrm;
    std::set<std::string> word_set;

    for (auto map_it = dict.cbegin(); map_it !=dict.cend(); ++map_it){
        auto key = map_it->first;
        auto key_it = key.crbegin();
        bool is_suffix = true;
        for(auto it = word.crbegin(); it!=word.crend(); ++it, ++key_it){
            if(key_it == key.crend() || tolower(*key_it) != tolower(*it)){
                is_suffix = false;
                break;
            }
        }
        if (is_suffix){
            word_set.insert(key);
        }
    }
    match_cnt = word_set.size();

    osstrm << match_cnt << std::endl;
    for(const auto &x: word_set){
        osstrm << x << std::endl;
    }
    osstrm << 0 << std::endl; // similar count
    return osstrm.str();
}

#endif //SOCKET_PROJECT_BACKEND_SERVER_H
