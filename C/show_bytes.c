#include <stdio.h>

typedef unsigned char *byte_pointer;


void show_bytes(byte_pointer start, size_t len){
    size_t i;
    for(i=0; i < len; ++i){
        printf(" %.2x", start[i]);
    }
    printf("\n");
}

/* 该函数用于实验扩展一个数字的位表示*/
void expand_a_number(){
    printf("==============2.2.6==============\n");
    printf("实验扩展一个数字的位表示\n");  
    short sx = -12345;          /*-12345*/
    unsigned short usx = sx;    /* 53191*/
    int x = sx;                 /*-12345*/
    unsigned ux = usx;          /* 53191*/

    printf("sx = %d:\t", sx);
    show_bytes((byte_pointer) &sx, sizeof(short));
    printf("usx = %u:\t", usx);
    show_bytes((byte_pointer) &usx, sizeof(unsigned short));
    printf("x = %d:\t", x);
    show_bytes((byte_pointer) &x, sizeof(int));
    printf("ux = %u:\t", ux);
    show_bytes((byte_pointer) &ux, sizeof(unsigned int));

    printf("===============end===============\n");
}


/* 该函数用于截断数字的实验 */
void truncate_numbr(){
    printf("==============2.2.7==============\n");
    int x = 53191;
    short sx = (short) x; /* -12345 */
    int y = sx;           /* -12345 */
    printf("x = %d:\t", x);
    show_bytes((byte_pointer) &x, sizeof(int));
    printf("sx = %d:\t", sx);
    show_bytes((byte_pointer) &sx, sizeof(short));
    printf("y = %d:\t", y);
    show_bytes((byte_pointer) &y, sizeof(int));
    printf("\n\n");

    int a = 0x80007fff;
    short ax = (short) a; 
    int b = ax;
    printf("ax = %d:", a);
    show_bytes((byte_pointer) &a, sizeof(int));
    printf("ax = %d:\t", ax);
    show_bytes((byte_pointer) &ax, sizeof(short));
    printf("b = %d:\t", b);
    show_bytes((byte_pointer) &b, sizeof(int));
    printf("\n\n");
    printf("===============end==============\n");
}

int main(){
    expand_a_number();
    truncate_numbr();
}
