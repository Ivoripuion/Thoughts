#include<iostream.h>
#include<winsock2.h>
#pragma comment(lib, "ws2_32.lib")
void msg_display(char * buf)
{
	char msg[200];
	strcpy(msg,buf);// overflow here, copy 0x200 to 200
	cout<<"********************"<<endl;
	cout<<"received:"<<endl;
	cout<<msg<<endl;
}
void main()
{
	int sock,msgsock,lenth,receive_len;
	struct sockaddr_in sock_server,sock_client;
	char buf[0x200]; //noticed it is 0x200
	WSADATA wsa;
	WSAStartup(MAKEWORD(1,1),&wsa);
	if((sock=socket(AF_INET,SOCK_STREAM,0))<0)
	{
		cout<<sock<<"socket creating error!"<<endl;
		exit(1);
	}
	sock_server.sin_family=AF_INET;
	sock_server.sin_port=htons(7777);
	sock_server.sin_addr.s_addr=htonl(INADDR_ANY);
	if(bind(sock,(struct sockaddr*)&sock_server,sizeof(sock_server)))
	{
		cout<<"binging stream socket error!"<<endl;
	}
	cout<<"**************************************"<<endl;
	cout<<" exploit target server 1.0 "<<endl;
	cout<<"**************************************"<<endl;
	listen(sock,4);
	lenth=sizeof(struct sockaddr);
	do{
		msgsock=accept(sock,(struct sockaddr*)&sock_client,(int*)&lenth);
		if(msgsock==-1)
		{
			cout<<"accept error!"<<endl;
			break;
		}
		else
		do
		{
			memset(buf,0,sizeof(buf));
			if((receive_len=recv(msgsock,buf,sizeof(buf),0))<0)
			{
				cout<<"reading stream message erro!"<<endl;
				receive_len=0;
			}
			msg_display(buf);//trigged the overflow 0X200>200
		}while(receive_len);
		closesocket(msgsock);
	}while(1);
	WSACleanup();
}