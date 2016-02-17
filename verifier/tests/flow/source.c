int a,b,c;

void flow(int a){
	b = 0;
	c = 0;
	if (!a) {
		c = 1;
	}
	if (!c){
		b = 1;
	}
}

int main(){
	flow(0);
	return 0;
}
