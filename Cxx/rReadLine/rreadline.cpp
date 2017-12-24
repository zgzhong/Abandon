#include "rreadline.h"
#include <fstream>
#include <sstream>
#include <string>
#include <utility> 
#include <stack>
#include <unistd.h>
#include <iostream> 

using namespace std;


bool ReversedLineFile::open(){
    if( access(m_filePath.c_str(), F_OK)==-1 ){
        return false;
    }
    m_file.open(m_filePath, ios::in);
    m_file.seekg(0, m_file.end);
    m_fileOffset = m_file.tellg();

    if ( !m_file.is_open() ){
        return false;
    }
    return true;
}

void ReversedLineFile::close(){
    if (m_file.is_open())
        m_file.close();
}

bool ReversedLineFile::readLine(string &line){
    if (m_buffer.empty())
        fillBuffer();
    if (m_buffer.empty())
        return false;
     
    line = std::move(m_buffer.top());
    m_buffer.pop();
    return true;
}

void ReversedLineFile::fillBuffer(){
    if(m_fileOffset == 0)
        return;

    string tempStr;
    auto last_fileOffset = m_fileOffset;
    if (m_fileOffset-OFFSET_STEP > 0){
        m_file.seekg(m_fileOffset-OFFSET_STEP, m_file.beg);
        getline(m_file, tempStr); // ingore first line
    }
    else
        m_file.seekg(0, m_file.beg);
    
    m_fileOffset = m_file.tellg();
    
    while(m_file.tellg() < last_fileOffset){
        getline(m_file, tempStr);
        m_buffer.push(std::move(tempStr));
    }
}
