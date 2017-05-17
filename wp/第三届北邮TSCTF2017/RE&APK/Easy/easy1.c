#include<stdio.h>
#include<string.h> 
int ex(char c) {
	if(c>='0'&&c<='9') return c-'0';
	return c-'a'+10;
}
char nex(int i) {
	if(i<=9) return i+'0';
	return i+'a'-10;
}
char solve(char a0,char b0) {
	int a=ex(a0),b=ex(b0);
	int c=a*16+b;
	int d=c/64+(c%64)*4;
	return d;
}
int main() {
	char dl[50],dl2[50],bl[50],bl2[50];
	int i,s,a,b,c;
	strcpy(dl,"46420b083b084011254c6259215e290e61486014092b09584063194008\0");
	//strcpy(dl2,"0acec70576858d1f6b402c57ecd36403adc42c58c566c4164cef14cd\0");
	strcpy(dl2,"5396db1daad6d448b815fe85788965d2b612fb0950b750845d39829957\0");
	for(s=strlen(dl),i=0;i<s;i++) {
		a=ex(dl[i]);
		b=ex(dl2[i]);
		c=a^b;
		bl2[i]=nex(c);
		printf("%d %d %d\n",a,b,c);
	}
	bl2[i]='\0';
	puts(bl2);
	for(i=0;i<s;i+=2) {
		printf("%c%c ",bl2[i],bl2[i+1]);
		bl[i/2]=solve(bl2[i],bl2[i+1]);
	}
	bl[i/2]='\0';
	puts(bl);
	system("pause") ;
	return 0;
}
