//#include "stdafx.h"
#include <WINSOCK2.H>
#include <stdio.h>
#include<string.h>
#include<windows.h>

#pragma  comment(lib,"ws2_32.lib")

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
    serAddr.sin_port = htons(42222);
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
	




	int a=0,b=0,i,j,t;
    while(1)
    {
		Sleep(100);
		ret = recv(sclient, response, 1500, 0);
		response[ret] = 0x00;
		printf("%d-- %s ret = %d\n",count++,response,ret); 
		if(!ret) break;

		a = 0; b= 0; t = 1;
		for(i=ret-1;i>=0;i--) {
			if(response[i]=='\n')
				if(response[i-1]>='0'&&response[i-1]<='9') {
					j=i-1;
					while(response[j]>='0'&&response[j]<='9'){
						b+=t*(response[j]-'0');
						t*=10;
						j--;
					}
					j--; t=1;
					while(response[j]>='0'&&response[j]<='9'){
						a+=t*(response[j]-'0');
						t*=10;
						j--;
					}
				}
		}
		printf("%d,%d\n",a,b);
		sendbuf = solve(a,b);
		sprintf(sendData,"%d\n",sendbuf);
		puts(sendData);
		send(sclient,sendData,strlen(sendData),0);
		
    }
	puts(response);
    closesocket(sclient);
    WSACleanup();
    return 0;
}

