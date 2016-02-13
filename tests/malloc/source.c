#include <stdio.h>
#include <stdlib.h>

unsigned int page_alloc(int num_of_ints){
  int* ret = (int*) malloc( num_of_ints << 2 );
  if ( ret == NULL ) return 0;
  return (int) ret; 
}

int main(){
  unsigned int page_address = page_alloc(100);

  //** page_address 0 !=

  printf("%d\n", page_address); 
  return 0; 
}
