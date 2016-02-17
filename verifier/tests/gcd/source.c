int gcdr ( int a, int b )
{
  if ( a==0 ) return b;
  return gcdr ( b%a, a );
}


int main(){
	return gcdr(4,6);
}
