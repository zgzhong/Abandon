#include "rreadline.h"
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char *argv[]){
    if (argc !=2 )
        return 0;
    ReversedLineFile f(argv[1]);
    if ( !f.open() ){
        cout << "open failed" << endl;
        return 0;
    }
    string s;
    while(true){
        if (!f.readLine(s))
            break;
        cout << s << endl;
    }
}
