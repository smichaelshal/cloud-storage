#django
from django.shortcuts import render
from django.contrib.auth.models import User

#models
from .models import File, Directory, Profile, LastAction


#rest_framework
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

import secrets
import ast

class UploadFileApi(generics.GenericAPIView):
    """
        class of upload files to server
    """
    def post(self, request, *args, **kwargs):
        """
            build objects on DB to the new files or retrieval existing files.
            parmas: request,
            return response http 200 Ok with:
                                                1. id of file
                                                2. last seek of file
        """
        retData = {}
        seekFile = 0
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        isFirstUploadFile = request.data['is_first']

        if isFirstUploadFile == '1':
       
            idNewFile = secrets.token_hex(16) #16 --> 64

            name_file = request.data['name_file']
            type_file = request.data['type_file']
            size_file = request.data['size_file']
            pathDestination = request.data['pathDestination']
            pathSource = request.data['pathSource']

            newFile = File()
            newFile.name_file = name_file
            newFile.type_file = type_file
            newFile.size_file = size_file
            newFile.user_upload = user
            newFile.seek_file = 0
            newFile.pathDestination = pathDestination
            newFile.pathSource = pathSource
            newFile.id_file = idNewFile
            newFile.save()
            
            LastActionProfile = LastAction(name_action='up', object_active=newFile, is_end_action=False, counter=0)
            LastActionProfile.save()
            
            profileUser.last_upload = LastActionProfile
            profileUser.save()

            tempListDirectory = pathDestination.split('/')
            listDirectory = list(filter(lambda i: i != '', tempListDirectory))

            self.addFileToDirectory(profileUser.root_directory, listDirectory, newFile)

        else:
            last_upload = profileUser.last_upload
            fileUpload = last_upload.object_active
            idNewFile = fileUpload.id_file
            seekFile = last_upload.counter

        retData = {
            "file": "Creation is successfully",
            "idFile": idNewFile,
            "seekFile": seekFile
            }
        return Response(retData, status=HTTP_200_OK)

    def addFileToDirectory(self, root_directory, listDirectory, newFile):
        """
            Gets a file object, a file path list and a root directory object and puts
             the file in the appropriate folder by the path.
            
            params: 
                1. root directory of user
                2. list path of the destination path
                3. object of the file

            return None
                
        """
        if len(listDirectory) != 0:
            root_directory = root_directory.directories.get(name_directory=listDirectory[0])
            try:
                self.addFileToDirectory(root_directory, listDirectory[1:], newFile)
            except:
                root_directory.files.add(newFile)
                root_directory.save()

        else:
            root_directory.files.add(newFile)
            root_directory.save()

class CreatePathApi(generics.GenericAPIView):
    """
        class for building directory paths
    """
    def post(self, request, *args, **kwargs):
        """
            params post request,
            ????
        """
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)


        pathDestination = request.data['pathDestination']
        pathSource = request.data['pathSource']

        tempListDirectory = pathDestination.split('/')
        listDirectory = list(filter(lambda i: i != '', tempListDirectory))        

        self.createdPath(listDirectory, profileUser.root_directory, user, pathSource)

        return Response(retData, status=HTTP_200_OK)

    def createdPath(self, listDirectory, root_directory, user, pathSource):
        if len(listDirectory) == 0:
            return
        try:
            newRoot_directory = root_directory.directories.get(name_directory=listDirectory[0])
        except:
            newRoot_directory = Directory(name_directory=listDirectory[0], size_directory=0, user_upload=user,
            pathDestination=self.getPath(root_directory.pathDestination, listDirectory[0]),
            pathSource=pathSource,id_directory=secrets.token_hex(16))
            
            newRoot_directory.save()
            
            root_directory.directories.add(newRoot_directory)
            root_directory.save()
        self.createdPath(listDirectory[1:], newRoot_directory, user, pathSource)

    def getPath(self, pathSource, folder):
        if pathSource[-1] == '/':
            return pathSource + folder
        else:
            return pathSource + '/' + folder
        
        
class GetStructDirectry(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        pathDestination = request.data['pathDestination']
        pathSource = request.data['pathSource']



        arrPath = pathSource.split('/')
        listDirectory = list(filter(lambda i: i != '', arrPath))
        
        objDirectry = GetDirectry(listDirectory, profileUser.root_directory)

        rooDirectory = profileUser.root_directory
        listRet = []
        
        self.getListDirectories(objDirectry, listRet, arrPath)


        retData = {
            "listPathsDirectories": listRet
        }

        return Response(retData, status=HTTP_200_OK)

    def getListDirectories(self, directory, listRet, arrPath):

        if len(directory.directories.all()) == 0:
            listRet.append(directory.pathDestination)
        else:
            listDirectory = directory.directories.all()
            for directoryNow in listDirectory:
                self.getListDirectories(directoryNow, listRet, arrPath)

class GetListFilesDirectories(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        pathSource = request.data['pathSource']
        tempListDirectory = pathSource.split('/')
        listDirectory = list(filter(lambda i: i != '', tempListDirectory))
        try:
            objDirectry = GetDirectry(listDirectory, profileUser.root_directory)
        except:
            retData = {
                "listFiles": []
            }
            return Response(retData, status=HTTP_200_OK)
        listFilesObjects = objDirectry.files.all()
        listFiles = []

        for file in listFilesObjects:
            listFiles.append({
                "idFile": file.id_file,
                "nameFile": file.name_file,
                "typeFile": file.type_file,
                "sizeFile": file.size_file,
            })

        retData = {
            "listFiles": listFiles
        }

        return Response(retData, status=HTTP_200_OK)

class GetLastUpload(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)
        try:
            retData = {
                "pathDestination": profileUser.last_upload.object_active.pathDestination
                }
        except:
           retData = { "pathDestination" : "NONE"}
     

        return Response(retData, status=HTTP_200_OK)

    
class GetLastDownload(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        retData = {
            "pathSource": profileUser.last_download.object_active.pathSource
        }

        return Response(retData, status=HTTP_200_OK)


   
class GetListDirectoriesApi(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        pathSource = request.data['pathSource']

        tempListDirectory = pathSource.split('/')
        listDirectory = list(filter(lambda i: i != '', tempListDirectory))
        objDirectry = GetDirectry(listDirectory, profileUser.root_directory)
        listDirectoryObjects = objDirectry.directories.all()
        listFiles = []

        for directory in listDirectoryObjects:
            listFiles.append({
                "name_directory": directory.name_directory,
                "size_directory": directory.size_directory,
                "pathDestination": directory.pathDestination,
            })

        retData = {
            "listDirectories": listFiles
        }


        return Response(retData, status=HTTP_200_OK)

class GetDirectoriesTree(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        pathSource = request.data['pathSource']

        return Response(retData, status=HTTP_200_OK)

class ChnageNameObject(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        dataFromClient = request.data["data"]

        isFile = dataFromClient['isFile'] # true == '1', false == '0'
        pathSource = dataFromClient['pathSource']
        newName = dataFromClient['newName']

        arrPath = pathSource.split('/')
        listDirectory = list(filter(lambda i: i != '', arrPath))
        

        DirectorySource = GetDirectry(listDirectory, profileUser.root_directory)
        if not self.IsOkNameObject(DirectorySource, newName, isFile):
            retData = {
                'error_name': 'the name used'
            }
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        if isFile == '1':
            idFile = dataFromClient['idFile']
            objectFile = DirectorySource.files.get(id_file=idFile)
            objectFile.name_file = newName
            objectFile.save()
            
        else:
            path = dataFromClient['path']
            pathList = path.split('/')
            listDirectory = list(filter(lambda i: i != '', pathList))
            r1 = DirectorySource.directories.get(name_directory=listDirectory[-1])
            r1.name_directory = newName
            oldPath = r1.pathDestination
            oldListPath = oldPath.split('/')
            oldListPath[-1] = newName
            newPath = '/'.join(oldListPath)
            if newPath[:2] == '//':
                newPath = newPath[1:]
            r1.pathDestination = newPath
            r1.save()

            indexDirectory = len(oldListPath) - 1

            self.changePaths(indexDirectory, r1, newName)


        return Response(retData, status=HTTP_200_OK)


    def changePaths(self, indexDirectory, rootDirectory, newName):
        listDirs = rootDirectory.directories.all()
        for subDirectory in listDirs:
            listSubPath = (subDirectory.pathDestination).split('/')
            listSubPath[indexDirectory] = newName
            subDirectory.pathDestination = '/'.join(listSubPath)
            if subDirectory.pathDestination[:2] == '//':
                subDirectory.pathDestination = subDirectory.pathDestination[1:]

            subDirectory.save()

            if len(subDirectory.directories.all()) > 0:
                self.changePaths(indexDirectory, subDirectory, newName)
                # self.rec(indexDirectory, subDirectory, newName)

    def IsOkNameObject(self, objDirectry, newName, isFile):
        if isFile == '1':
            listFilesObjects = objDirectry.files.all()
            for file in listFilesObjects:
                if file.name_file == newName:
                    return False
        else:
            listDirectoriesObjects = objDirectry.directories.all()
            for directory in listDirectoriesObjects:
                if directory.name_directory == newName:
                    return False
        return True

def GetDirectry(listPath, rootDirectory):
        if len(listPath) == 0:
            return rootDirectory
        else:
            rootDirectory = rootDirectory.directories.get(name_directory=listPath[0])
            return GetDirectry(listPath[1:], rootDirectory)

class DeleteObject(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        try:
            pathSource = request.data["data"]['pathSource']
            isDirectory = request.data["data"]['isDirectory'] # 1 == True 0 == False

        
            tempListDirectory = pathSource.split('/')[:-1]
            listDirectory = list(filter(lambda i: i != '', tempListDirectory))
        except:
            retData = {
                "listFiles": []
            }
            return Response(retData, status=HTTP_200_OK)
        
        try:
            objDirectry = GetDirectry(listDirectory, profileUser.root_directory)
        except:
            retData = {
                "listFiles": []
            }
            return Response(retData, status=HTTP_200_OK)
        try:
            if isDirectory == '1':
                pathSource = request.data["data"]['pathSource']
                tempListDirectoryToDelete = pathSource.split('/')
                listDirectoryToDeletes = tempListDirectoryToDelete[1:]
                objDirectryToDelete = GetDirectry(listDirectoryToDeletes, profileUser.root_directory)


                objDirectry.directories.remove(objDirectryToDelete)
                profileUser.deleted_directory.directories.add(objDirectryToDelete)

                retData = {'isSuccess': True}
            else:
                idFile = request.data["data"]['idFile']

                fileObject = objDirectry.files.get(id_file=idFile)

                objDirectry.files.remove(fileObject)
                profileUser.deleted_directory.files.add(fileObject)

                retData = {'isSuccess': True}
        except:
            retData = {
                "listFiles": []
            }
            return Response(retData, status=HTTP_200_OK)

        return Response(retData, status=HTTP_200_OK)
    
    def GetDirectry(listPath, rootDirectory):
        if len(listPath) == 0:
            return rootDirectory
        else:
            rootDirectory = rootDirectory.directories.get(name_directory=listPath[0])
            return GetDirectry(listPath[1:], rootDirectory)

class ShareObject(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        dataFromClient = request.data["data"]

        pathSource = dataFromClient["pathSource"]
        listUsersNames = dataFromClient["listUsers"]
        idObject = dataFromClient["id"]
        isFile = dataFromClient["isFile"] # true == '1', false == '0'

        arrPath = pathSource.split('/')
        listDirectory = list(filter(lambda i: i != '', arrPath))

        objDirectry = GetDirectry(listDirectory, profileUser.root_directory)
        listObjectsUsers, listFailds = CreateListUsers(listUsersNames)


        if isFile == '1':
            objectToAdd = objDirectry.files.get(id_file=idObject)                
            addObjectToUser(listObjectsUsers, objectToAdd, True)
        else:
            addObjectToUser(listObjectsUsers, objDirectry, False)

        return Response(retData, status=HTTP_200_OK)
        

    def GetDirectry(listPath, rootDirectory):
        if len(listPath) == 0:
            return rootDirectory
        else:
            rootDirectory = rootDirectory.directories.get(name_directory=listPath[0])
            return GetDirectry(listPath[1:], rootDirectory)


def addObjectToUser(listUsers, objectToAdd, isFile):
    if isFile:
        # try:
        #     user.profile.root_directory.files.get(id_file=idFile)
        #     print('g1')
        #     return
        # except:
        #     print('g2')
        for user in listUsers:
            user.profile.root_directory.files.add(objectToAdd)
    else:
        for user in listUsers:
            user.profile.root_directory.directories.add(objectToAdd)


class GetIdsUsers(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        retData = {}
        try:
            strTokenUser = request.headers["Authorization"].split(' ')[1]
            user = Token.objects.all().filter(key=strTokenUser)[0].user
            profileUser = user.profile
        except:
            retData = {'Token': 'The token is incorrect'}
            return Response(retData, status=HTTP_400_BAD_REQUEST)

        dataFromClient = request.data["data"]
        listUsers = dataFromClient["listUsers"]
        listObjectsUsers, listFailds = CreateListUsers(listUsers)
        listIds = getlistIdUserObjects(listObjectsUsers)
        print("listFailds: ", listFailds)

        retData = {'listIds': listIds, 'listFailds': listFailds}

        return Response(retData, status=HTTP_200_OK)


def CreateListUsers(listUsers):
        listObjectsUsers = []
        listFailds = []
        for user in listUsers:
            try:
                if user != "admin":
                    userObject = User.objects.get(username=user)
                    listObjectsUsers.append(userObject)
                else:
                    listFailds.append(user)
            except:
                listFailds.append(user)
        return listObjectsUsers, listFailds

def getlistIdUserObjects(listUserObj):
    listId = []
    for user in listUserObj:
        listId.append(user.id)
    return listId