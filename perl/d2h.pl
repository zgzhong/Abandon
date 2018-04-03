#!/usr/bin/env perl
# Convert list to decimal numbers into hex


for($i=0; $i < @ARGV; $i++){
    printf("%d=0x%x\n",  $ARGV[$i], $ARGV[$i]);
}
