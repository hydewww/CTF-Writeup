//#include "stdafx.h"
#include <WINSOCK2.H>
#include <stdio.h>
#include<string.h>
#include<windows.h>

#pragma  comment(lib,"ws2_32.lib")


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
    serAddr.sin_port = htons(43333);
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
		Sleep(3);
		ret = recv(sclient, response, 1500, 0);
		if(!ret) break;
		else if(ret<=22) continue;
		response[ret] = 0x00;
		printf("%d-- %s ret = %d\n",count++,response,ret); 

		if(count==1&&strstr(response,"Round")==NULL) continue;
		if(strstr(response,"left")==NULL) {
			for(i = ret-1; i>=0 ;i--) 
				if(response[i+1]=='\n'||response[i+1]=='\0')
			if(response[i]>='0'&&response[i]<='9')
			{
					j=i;

					t=1;a=b=0;

					while(response[j]!=' '){
						b+=(response[j]-'0')*t;
						t*=10;
						j--;
					}

					t=1; j--;
					while(response[j]>='0'&&response[j]<='9'){
						a+=(response[j]-'0')*t;
						t*=10;
						j--;
					}
					break;
				}
			if(i<=0) continue;
			}
		else {
		//	puts(response);
		//	printf("res = %d\n",ret);
			i = 0;
			while(i<ret&&(response[i]>'9'||response[i]<'0')) i++;
			if(i<ret&&response[i]>='0'&&response[i]<='9') {
				a=0;
			   while(response[i]>='0'&&response[i]<='9'){
				a=a*10+(response[i]-'0');
				i++;
				}
			}
		}
				
		printf("%d %d\n",a,b);
		if(a<=b) {
			sprintf(sendData,"%d\n",a);
		    a = 0;
		}
		else {
			
			  sprintf(sendData,"%d\n",a%(b+1));
					
		}
		
		puts(sendData),
		send(sclient,sendData,strlen(sendData),0);
		
		strcpy(sendData,"");
		//send(sclient,sendData,strlen(sendData),0);
    }
	puts(response);
    closesocket(sclient);
    WSACleanup();
    return 0;
}
