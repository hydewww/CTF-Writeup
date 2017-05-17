// crackme.cpp : Defines the entry point for the console application.
//

//#include "stdafx.h"

#include <math.h>
#include <Windows.h>
#include<stdio.h>
#include<time.h>
#define N 1005
double Rn,Xn=2681,R[N];
double Lamda=pow(5,5), M=pow(2,35)-31;
void Rnd()
{	Xn=fmod((Lamda*Xn),M); 
	Rn=Xn/M;
	printf("%lf  ",Rn);
}

unsigned long pow_mod(unsigned long vsn, unsigned int e)
{
	unsigned __int64 v4; // [sp+4Ch] [bp-Ch]@1
	unsigned int i; // [sp+54h] [bp-4h]@1

	i = 0;
	v4 = (long long)1;
	//printf("v4 = %lld\n",v4);
	if (e && vsn)
	{
		for (i = 0; i < e; ++i)
			v4 = v4 * (unsigned __int64)vsn % 0xFFFFFFFF;
	}
	else
	{
		v4 = vsn != 0;
	}
	return (unsigned long)v4;
}

unsigned long get_ulong(char *str, int radix)
{
	char temp[9] = { 0 };
	memcpy(temp, str, 8);
	return strtoul(temp, 0, radix);
}
unsigned c1[64000];
int count1;

unsigned long km(unsigned long v4,unsigned long b){
	unsigned __int64 p,s,a = (unsigned __int64)v4;
	p = 0xFFFFFFFF;
	// A^B %p
	s=a; a=1;
	while(b)
	{
		if(b%2)a=(a*s)%p;
		s=(s*s)%p;
		b/=2;
		
	}
	return (unsigned long)a;
}
void solve2() {
	unsigned long m1=0x1,m2=0x1,e=0x2a,d;
	unsigned long ans1=0x84a721f4,ans2=0x1133086,q=0x1000000;
	unsigned __int64 v4=(long long)1,v5=(long long)1;
	for(d=1;d<0xffffffff;d++) {
		//v4 * (unsigned __int64)vsn % 0xFFFFFFFF;
		v4 = v4 * (unsigned __int64)ans1 % 0xFFFFFFFF;
		v5 = v5 * (unsigned __int64)ans2 % 0xFFFFFFFF;
		m1=(unsigned long)v4;
		m2=(unsigned long)v5;
		e=(m1^m2)%q;
		if(e==(m1^m2)%q) {
			printf("Yes,m1=%x,m2=%x,d=%x",m1,m2,d);
			if(km(m1,e)==ans1&&km(m2,e)==ans2) {
				printf("Yes,Yes,d=%x,m1=%x,m2=%x,e=%x\n",d,m1,m2,e);
				printf("ans = %x%x\n",m1,m2);
				return;
			}
		}
		//printf("%x %x %x",e,km(m1,e),km(m2,e));
		if(d%0xffffff==0) printf("AI,d=%x\n",d);
	}
}

int main(int argc, CHAR* argv[])
{
	char sn[32] = { 0 };
	printf("ÉîË¼Êý¶Ü CTF 2017 CrackMe\n");

	solve2();

	printf("Please input serial:");
	scanf("%s", sn);

	unsigned long m1 = get_ulong(&sn[0], 16);
	unsigned long m2 = get_ulong(&sn[8], 16);
	
	printf("%x %x\n",m1,m2);

	unsigned long e = (m2 ^ m1) % 0x1000000;
	if (e > 2 && m1 && m2)
	{
		unsigned long c1 = pow_mod(m1, e);
		unsigned long c2 = pow_mod(m2, e);

		if ((c1 + c2) == 0x85ba527a && (c1 - c2) == 0x8393f16e)
		{
			printf("Congratulations, registration successful!\n\n");
			return 0;
		}
	}

	printf("Registration failed, try again!\n\n");
	return -1;
}

