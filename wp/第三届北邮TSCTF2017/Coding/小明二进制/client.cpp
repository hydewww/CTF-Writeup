//#include "stdafx.h"
#include <WINSOCK2.H>
#include <stdio.h>
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
    serAddr.sin_port = htons(41111);
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
    while(1)
    {
		//Sleep(100);
		ret = recv(sclient, response, 1500, 0);
		if(!ret) break;
		response[ret] = 0x00;
		printf("%d-- %s\n",count++,response);

		
		for(int i = strlen(response)-1;i>=0;i--)
			if(response[i]=='r') {
				//printf ("n %d\n",i);
				if(response[i-1]=='u') {
					//printf ("u %d\n",i);
					if(response[i-2]=='o') {
						//printf ("m %d\n",i);
						if(response[i-3]=='Y')
							if(response[i-4]=='\n'){
							          int j=i-5;
                                      sendbuf = 0;
                                      while(response[j]!='\n') {
                                          if(sendbuf<response[j])
                                              sendbuf = response[j];
                                          j--;
									  }
									  break;
									 
								}
							  
					}
				}
			}
			if(sendbuf)
			 //printf ("%d\n",sendbuf-48),
			 sprintf (sendData,"%d\n",sendbuf-48),
			 puts(sendData),
			 //Sleep(100),
			 send(sclient, sendData, strlen(sendData), 0),
			 strcpy(sendData,"");
    }
    closesocket(sclient);
    WSACleanup();
    return 0;
}
