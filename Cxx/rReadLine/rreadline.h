#ifndef RREADLINE_H_201712
#define RREADLINE_H_201712

#include <fstream>
#include <string>
#include <stack> 

class ReversedLineFile{
public:
    const int64_t OFFSET_STEP = 1<<28;
    ReversedLineFile(const std::string &fpath):m_filePath(fpath), m_fileOffset(0){}
    ~ReversedLineFile(void){
        close();
    }

    bool open();
    void close();
    bool readLine(std::string &line);

protected:
    void fillBuffer();
    
private:
    std::string              m_filePath;
    int64_t                  m_fileOffset;
    std::ifstream            m_file;
    std::stack<std::string> m_buffer; 
};

#endif
