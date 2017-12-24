#include "rreadline.h"
#include <fstream>
#include <sstream>
#include <string>
#include <utility> 
#include <stack>
#include <unistd.h>
#include <iostream> 

using namespace std;

char ReversedLineFile::m_buffer[ReversedLineFile::OFFSET_STEP+1];

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
    if (m_lineStack.empty())
        fillBuffer();
    if (m_lineStack.empty())
        return false;
     
    line = std::move(m_lineStack.top());
    m_lineStack.pop();
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
    m_file.read(m_buffer, last_fileOffset - m_fileOffset);
    m_buffer[last_fileOffset - m_fileOffset] = '\0'; 
    istringstream iss(m_buffer);
    
    while(getline(iss, tempStr)){
        m_lineStack.push(std::move(tempStr));
    }
}
