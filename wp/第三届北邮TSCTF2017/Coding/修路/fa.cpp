//#include "stdafx.h"
#include <WINSOCK2.H>
#include <stdio.h>
#include<string.h>
#include<windows.h>
#define MAXN 1005
#pragma  comment(lib,"ws2_32.lib")
int fa[MAXN],rank[MAXN];
void init(int n){for(int i=0;i<n;i++)fa[i]=i,rank[i]=0;}

int find(int x)
{	if(fa[x]==x)return x;
	return fa[x]=find(fa[x]);
} 

void unite(int x,int y)
{	x=find(x),y=find(y);
	if(x==y)return;
	if(rank[x]<rank[y])fa[x]=y;
	else
	{
		fa[y]=x;
		if(rank[x]==rank[y])rank[x]++;
	}
}
bool same(int x,int y){return find(x)==find(y);}

int solve(int a,int b){
	int s,p=10000;
	// A^B %p
	s=a; a=1;
	while(b)
	{
		if(b%2)a=(a*s)%p;
		s=(s*s)%p;
		b/=2;
		
	}
	return a;
}

int main()
{
    WORD sockVersion = MAKEWORD(2,2);
    WSADATA data; 
    if(WSAStartup(sockVersion, &data) != 0)
    {
        return 0;
    }

    SOCKET sclient = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
   if(sclient == INVALID_SOCKET)
    {
        printf("invalid socket !");
        return 0;
    }

    sockaddr_in serAddr;
    serAddr.sin_family = AF_INET;
    serAddr.sin_port = htons(44444);
    serAddr.sin_addr.S_un.S_addr = inet_addr("10.105.42.5"); 
    if (connect(sclient, (sockaddr *)&serAddr, sizeof(serAddr)) == SOCKET_ERROR)
    {
        printf("connect error !");
        closesocket(sclient);
        return 0;
    } 
    char sendData[1024] = "";
	int sendbuf=0;

    char response[102400];
    int ret ;
	int count = 0;
	




	int a=0,b=0,i,j,t,n=1000;
	init(n);
    while(1)
    {
		//Sleep(100);
		ret = recv(sclient, response, 15000, 0);
		response[ret] = 0x00;
		printf("%d-- %s ret = %d\n",count++,response,ret); 
		if(!ret) break;
		
		if(count==1) {
			sprintf(sendData,"\n"),
			send(sclient,sendData,strlen(sendData),0);
			continue;
			Sleep(100);
		}
		if(count==2) {
			int counte=0;
			for(i=0;i<ret;i=j+1) {
				a=0;
				j=i;
				if(response[j]=='W') break;
				if(response[j]>'9'||response[j]<'0') continue;
				while(response[j]<='9'&&response[j]>='0') {
					a=a*10+(response[j]-'0');
					j++;
				}
				counte++;
				if(counte%2) b=a;
				else 
					unite(a,b);
			}
			a=b=0;t=1;
			for(i=ret-1;i>=0;i--) {
				if(response[i]<='9'&&response[i]>='0') {
					while(response[i]<='9'&&response[i]>='0') {
						a+=t*(response[i]-'0');
						t*=10;
						i--;
					}
					while(i>=0&&!(response[i]<='9'&&response[i]>='0')) i--;
					if(i<0) a=0; 
					else 
					{
					  t=1; 
					  while(i>=0&&response[i]<='9'&&response[i]>='0') {
						b+=t*(response[i]-'0');
						t*=10;
						i--;
					  }
					  break;
					}
				}
			}
				
				printf("%d %d\n",a,b);
				if(a==0&&b==0) continue;
				sprintf(sendData,"%s\n",same(a,b)?"yes":"no");
				puts(sendData);
				send(sclient,sendData,strlen(sendData),0);
				Sleep(100);
		}
		else {
			//puts(response);
				a=b=0;t=1;
			for(i=ret-1;i>=0;i--) {
				//printf("%c\n",response[i]);
				if(response[i]<='9'&&response[i]>='0') {
					while(response[i]<='9'&&response[i]>='0') {
						a+=t*(response[i]-'0');
						t*=10;
						i--;
					}
					while(!(response[i]<='9'&&response[i]>='0')) i--;
					t=1; 
					while(response[i]<='9'&&response[i]>='0') {
						b+=t*(response[i]-'0');
						t*=10;
						i--;
					}
					break;
				}
			}	
				printf("%d %d\n",a,b);
				if(a==0&&b==0) continue;
				sprintf(sendData,"%s\n",same(a,b)?"yes":"no");
				puts(sendData);
				send(sclient,sendData,strlen(sendData),0);
			
		}
		/*printf("%d,%d\n",a,b);
		sendbuf = solve(a,b);
		sprintf(sendData,"%d\n",sendbuf);
		puts(sendData);
		send(sclient,sendData,strlen(sendData),0);
		*/
		
    }
	puts(response);
    closesocket(sclient);
    WSACleanup();
    return 0;
}

