#ifndef SOCKET_PROJECT_AWS_H
#define SOCKET_PROJECT_AWS_H

#include "global.h"
#include <set>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>

class Result {
public:
    Result() = default;
    ~Result() = default;

    Result(void*, Query *);
    explicit Result(const std::vector<Result>&);

    std::string to_client() const;
    std::string to_monitor() const;
    std::string similar_word() const {
        if (m_similar_cnt)
            return *m_similar_word_vec.cbegin();
        return "";
    }
    int get_match_cnt() const {return m_match_cnt;}
    int get_similar_cnt() const {return m_similar_cnt;}

private:
    Query *m_p_query;

    int m_match_cnt;
    int m_similar_cnt;
    std::set<std::string> m_match_set;
    std::vector<std::string> m_similar_vec;
    std::vector<std::string> m_similar_word_vec;
};

Result::Result(void *p, Query *p_query):m_match_cnt(0), m_similar_cnt(0), m_match_set(), m_similar_vec(), m_similar_word_vec(), m_p_query(p_query){
    std::istringstream iss((char*)p);
    std::string num;

    std::getline(iss, num);
    m_match_cnt = std::stoi(num);
    for(int i=0; i< m_match_cnt; ++i){
        std::string tmp;
        std::getline(iss, tmp);
        m_match_set.insert(tmp);
    }
    std::getline(iss, num);
    m_similar_cnt = std::stoi(num);
    for(int i=0; i < m_similar_cnt; ++i){
        std::string word;
        std::string definition;
        std::getline(iss, word);
        std::getline(iss, definition);

        m_similar_word_vec.push_back(word);
        m_similar_vec.push_back(definition);
    }
}

Result::Result(const std::vector<Result> &result_vec):m_match_cnt(0), m_similar_cnt(0), m_match_set(), m_similar_vec(), m_similar_word_vec(), m_p_query(nullptr) {
    for(const Result &item: result_vec){
        m_p_query = item.m_p_query;

        m_match_set.insert(item.m_match_set.begin(), item.m_match_set.end());
        m_similar_vec.insert(m_similar_vec.end(), item.m_similar_vec.begin(), item.m_similar_vec.end());
        m_similar_word_vec.insert(m_similar_word_vec.end(), item.m_similar_word_vec.begin(), item.m_similar_word_vec.end());
    }

    m_match_cnt = m_match_set.size();
    m_similar_cnt = m_similar_vec.size();
}


std::string Result::to_client() const {
    std::ostringstream oss;
    if(m_match_cnt == 0){
        oss << "Found no matches for <" << m_p_query->m_input << ">" << std::endl;
    }
    else {
        if (m_p_query->m_type == search){
            oss << "Found a matches for <" << m_p_query->m_input << "> :\n";
            oss << "<" << *m_match_set.cbegin() << ">" << std::endl;
        }
        else {
            oss << "Found < " << m_match_cnt << "> matches for <" << m_p_query->m_input << "> :\n";

            for (const auto &x: m_match_set) {
                oss << "<" << x << ">" << std::endl;
            }
        }
    }
    return oss.str();
}

std::string Result::to_monitor() const {
    std::ostringstream oss;

    if (m_p_query->m_type == search){
        if (m_match_cnt == 0){
            oss << "Found no matches for <" << m_p_query->m_input << ">" << std::endl;
        }
        else{
            oss << "Found a matches for <" << m_p_query->m_input << ">: \n";
            oss << "<" << *m_match_set.cbegin() << ">" << std::endl;

            if (m_similar_cnt != 0){
                oss << "One edit distance match is ";
                oss << "<" << *m_similar_word_vec.cbegin() << ">" << std::endl;
                oss << "<" << *m_similar_vec.cbegin() << ">" << std::endl;
            }
        }
    }
    else{
        if(m_match_cnt == 0){
            oss << "Found no matches for " << m_p_query->m_input << ">" << std::endl;
        }
        else {
            oss << "Found <" << m_match_cnt << "> matches for <" << m_p_query->m_input << ">:\n";
            for (const auto &x: m_match_set) {
                oss << "< " << x << " >" << std::endl;
            }
        }
    }

    return oss.str();
}

#endif //SOCKET_PROJECT_AWS_H
