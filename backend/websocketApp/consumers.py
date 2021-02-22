from channels.consumer import AsyncConsumer
import secrets
from django.conf import settings
import os
import json
from aiofile import async_open

from channels.db import database_sync_to_async
from filesApp.models import Profile, File, LastAction
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class UploadConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.GLOBAL_PATH = str(settings.BASE_DIR) + '/LibraryFiles/filesUpload/'
        self.token = None
        self.pathSource = None
        self.pathDestination = None
        self.idFile = None
        self.flag = None
        self.PATH_FILE = None
        self.FILE = None
        self.isAuth = None
        self.isFirst = True
        self.user = None
        self.isDone = None

        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        dataFile = None
        msgToClient = "NAK"
        if self.isAuth or self.isAuth == None:
            if self.isFirst:
                dataFromClientText =  event["text"]
                dictUser = json.loads(dataFromClientText)
                self.flag = 'S'
                self.isFirst = False
            else:
                dataFromClientBytes = event['bytes']
                self.flag = chr(dataFromClientBytes[0])
                dataFile = dataFromClientBytes[1:]

            if self.flag == "S":
                self.token = dictUser['token']
                self.isAuth = await self.isAuthFunc(self.token)
                if self.isAuth:
                    self.user = await self.getUser(self.token)
                    self.pathSource = dictUser['pathSource']
                    self.pathDestination = dictUser['pathDestination']
                    self.idFile = dictUser['idFile']
                    self.PATH_FILE = self.GLOBAL_PATH + self.idFile
                    self.FILE = open(self.PATH_FILE, 'ab')
                    self.isDone = False
                    msgToClient = "ACK-S"

            elif self.flag == "C":
                self.FILE.write(dataFile)
                msgToClient = "ACK-C"
            elif self.flag == "E":
                self.FILE.close()
                self.isDone = True
                await self.saveSeek()
                msgToClient = "ACK-E"
            elif self.flag == "A":
                pass

    
        await self.send({
            "type": "websocket.send",
            "text": msgToClient,
        })
    
    async def websocket_disconnect(self, event):
        if not self.isDone:
            await self.saveSeek()
        msg = 'N'
        if self.isDone == True:
            msg = 'Y'
        await self.send({
            "type": "websocket.send",
            "text": msg,
        })

    @database_sync_to_async
    def isAuthFunc(self, tokenUser):
        listToken = Token.objects.all().filter(key=tokenUser)
        if len(listToken) == 0:
            return False
        return True
    @database_sync_to_async
    def getUser(self, token):
        return Token.objects.all().filter(key=token)[0].user
    
    @database_sync_to_async
    def saveSeek(self):
        sizeFile = os.path.getsize(self.PATH_FILE)
        p1 = self.user.profile
        if p1.last_upload.counter != 0:
            fileActive = File.objects.get(id_file=self.idFile)

            LastActionProfile = LastAction(name_action='up', object_active=fileActive, is_end_action=False, counter=sizeFile)
            LastActionProfile.save()
            
            p1.last_upload = LastActionProfile
            p1.save()
        else:
            p1.last_upload.counter = sizeFile
            p1.last_upload.save()
            p1.save()

class DownloadConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        self.token = None
        self.pathSource = None
        self.pathDestination = None
        self.idFile = None
        self.seekFile = None
        self.flag = None
        self.CHUNK = 1024*1024
        self.PATH_FILE = None
        self.FILE = None
        self.GLOBAL_PATH = str(settings.BASE_DIR) + '/LibraryFiles/filesUpload/'
        self.isFirst = True
        self.isAuth = None
        self.user = None

        await self.send({
            "type": "websocket.accept",
        })

    async def websocket_receive(self, event):
        dataFromFile = b'S'
        dataFromClientText =  event["text"]
        if self.isAuth == None or self.isAuth:
            if self.isFirst:
                dictUser = json.loads(dataFromClientText)
                self.token = dictUser['token']
                self.isAuth = await self.isAuthFunc(self.token)
                if self.isAuth:
                    self.user = await self.getUser(self.token)
                    self.pathSource = dictUser['pathSource']
                    self.pathDestination = dictUser['pathDestination']
                    self.idFile = dictUser['idFile']
                    self.seekFile = dictUser['seekFile']
                    self.PATH_FILE = self.GLOBAL_PATH + self.idFile
                    self.FILE = open(self.PATH_FILE, 'rb')
                self.isFirst = False
            else:
                self.flag = dataFromClientText[0]
                self.seekFile = int(dataFromClientText[1:])
                self.FILE.seek(self.seekFile)
                dataFromFile = self.FILE.read(self.CHUNK)
                if len(dataFromFile) == 0:
                    dataFromFile = b'E'
                else:
                    dataFromFile = b'C' + dataFromFile
        else:
            dataFromFile = b'R'
        await self.send({
            "type": "websocket.send",
            "bytes": dataFromFile,
        })
    
    async def websocket_disconnect(self, event):
        if self.FILE != None:
            self.FILE.close()
            await self.saveDownload()
       
        await self.send({
            "type": "websocket.send",
        })

    @database_sync_to_async
    def isAuthFunc(self, tokenUser):
        listToken = Token.objects.all().filter(key=tokenUser)
        if len(listToken) == 0:
            return False
        return True
    @database_sync_to_async
    def getUser(self, token):
        return Token.objects.all().filter(key=token)[0].user

    @database_sync_to_async
    def saveDownload(self):
        p1 = self.user.profile
        fileActive = File.objects.get(id_file=self.idFile)

        LastActionProfile = LastAction(name_action='down', object_active=fileActive, is_end_action=False, counter=self.seekFile)
        LastActionProfile.save()
        
        p1.last_download = LastActionProfile
        p1.save()

# class MessageConsumer(AsyncConsumer):
#     async def websocket_connect(self, event):
#         self.token = None
#         self.isFirst = True
#         self.flag = None
#         self.isAuth = None
#         self.user = None
#         self.isLogout = False
        
#         await self.send({
#             "type": "websocket.accept",
#         })

#     async def websocket_receive(self, event):
#         dataFromClientText =  event["text"]
#         if self.isFirst:
#             self.token = dataFromClientText
#             self.flag = 'S'
#             self.isFirst = False
#             self.isAuth = await self.isAuthFunc(self.token)
#             if self.isAuth:
#                 self.user = await self.getUser(self.token)
#         else:
#             pass
#         await self.send({
#             "type": "websocket.send",
#         })


#     async def websocket_disconnect(self, event):
#         if self.isAuth:
#             self.isLogout = await self.logoutUser()
#         await self.send({
#             "type": "websocket.send",
#         })
    
#     @database_sync_to_async
#     def isAuthFunc(self, tokenUser):
#         listToken = Token.objects.all().filter(key=tokenUser)
#         if len(listToken) == 0:
#             return False
#         return True
#     @database_sync_to_async
#     def getUser(self, token):
#         return Token.objects.all().filter(key=token)[0].user

#     @database_sync_to_async
#     def logoutUser(self):
#         self.user.auth_token.delete()

#         profileUser = self.user.profile
#         profileUser.is_active = False
#         profileUser.save()

#         return True

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = None
        self.room_group_name = None

        self.token = None
        self.isFirst = True
        self.flag = None
        self.isAuth = None
        self.user = None
        self.isLogout = False

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        if self.isAuth:
            self.isLogout = await self.logoutUser()

        try:
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )
        except:
            pass

    # Receive message from WebSocket
    async def receive(self, text_data): 
        
        text_data_json = json.loads(text_data)        

        typeOfMsg = text_data_json['type']

        if self.isFirst:
            self.token = text_data_json['token']
            self.flag = 'S'
            self.isFirst = False
            self.isAuth = await self.isAuthFunc(self.token)
            if self.isAuth:
                self.user = await self.getUser(self.token)
        else:
            pass
        
        if typeOfMsg == 'connect':
            self.room_name = self.scope['url_route']['kwargs']['room_name']
            self.room_group_name = 'chat_%s' % self.room_name

            # Join room group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
        elif typeOfMsg == 'directory':
            message = text_data_json['msg']
            list_ids = text_data_json['ids']

            # Send message to room group
            for idGroup in list_ids:
                await self.channel_layer.group_send(
                    # self.room_group_name,
                    f'chat_{idGroup}',
                    {
                        'type': 'chat_message',
                        'message': message,
                        'typeMsg': 'directory'
                    }
                )

        elif typeOfMsg == 'share':
            pass

       
    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        typeMsg = event['typeMsg']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'typeMsg': typeMsg
        }))
       
    @database_sync_to_async
    def isAuthFunc(self, tokenUser):
        listToken = Token.objects.all().filter(key=tokenUser)
        if len(listToken) == 0:
            return False
        return True
    @database_sync_to_async
    def getUser(self, token):
        return Token.objects.all().filter(key=token)[0].user

    @database_sync_to_async
    def logoutUser(self):
        self.user.auth_token.delete()

        profileUser = self.user.profile
        profileUser.is_active = False
        profileUser.save()

        return True