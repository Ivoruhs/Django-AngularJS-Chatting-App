from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.aggregates import Min, Max
from django.db.models.expressions import F
from django.db.models.query_utils import Q
from django.shortcuts import render, render_to_response, redirect
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import UserInfo
from chatbox.settings import MEDIA_URL
from chats.serializers import *



@login_required(login_url='signin')
def inbox(request):
    userList = User.objects.all()
    context={'userList' : userList,"activeUserName": request.user.username, "activeUserId": request.user.id, "mediaUrl": MEDIA_URL}
    return render(request, 'chats/inbox.html', context)




#API Views
class UserAPIView(APIView):

    renderer_classes = (JSONRenderer,)
    def get(self,request):
        """
        :param request: 
        :return: All users' list excluding the current user
        """

        users = User.objects.filter(~Q(id = request.user.id))
        serializer=UserSerializer(users, many=True)
        return Response(serializer.data)





class MessageAPIView(APIView):

    renderer_classes = (JSONRenderer,)
    def get(self,request):
        """
        Returns message list
        :param request: receiver userId or message tobeDeletedId or message tobeArchivedId
        :return: if receiver userId then returns existing messages with the receiver. Otherwise returns
        all messages of active user. If tobeDeletedId then delete message. If tobeArchivedId then archive message.
        """
        userId = request.GET.get('userId', 0)
        tobeDeletedId = request.GET.get('tobeDeletedId', 0)
        tobeArchivedId = request.GET.get('tobeArchivedId', 0)

        if userId != 0 :
            userObj = User.objects.get(pk=userId)
            messages= Message.objects.filter(Q(sender =request.user, receiver= userObj)| Q(sender =userObj, receiver= request.user))
            serializer = UserMessageSerializer(messages, many=True)
            return Response(serializer.data)

        elif tobeDeletedId != 0:
            deleteResult = Message.objects.filter(id=tobeDeletedId).delete()
            return Response([])

        elif tobeArchivedId != 0:
            archiveResult = Message.objects.get(pk= tobeArchivedId)
            archiveResult.isArchive = True
            archiveResult.save()
            return Response([])


        messages = Message.objects.filter(Q(sender=request.user) | Q(receiver_id=request.user))
        serializer=UserMessageSerializer(messages, many=True)
        return Response(serializer.data)





class SendMessageAPIView(APIView):
    """
    Send message to another user
    """
    def post(self, request, format=None):
        userObj= User.objects.get(pk= request.data['receiver'])
        messageObj= {}
        messageObj['receiver'] =  userObj.id
        messageObj['sender'] = request.user.id

        serializer = MessageSerializer(data=messageObj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






class ConversationAPIView(APIView):
    renderer_classes = (JSONRenderer,)

    def get(self, request):
        """
        returns conversation of current with another user
        :param request: existingUserMessageId
        :return: if existingUserMessageId exists returns existing message
        """

        existingMessageId = request.GET.get('existingUserMessageId', 0)

        if existingMessageId != 0:
            conversations = Conversation.objects.filter(messageId = existingMessageId)
            serializer = ConversationSerializer(conversations, many=True)
            return Response(serializer.data)


    def post(self, request, format=None):
        """
        :param request: messageObj
        :param format: {text:"", messageId:"",author:""}
        :return: Saves conversation and returns saving feedback
        """

        convoObj= {}
        convoObj['author']= request.user.id
        convoObj['text']= request.data['text']
        convoObj['messageId'] = request.data['messageId']
        serializer = ConversationSerializer(data=convoObj)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class UserConversationAPIView(APIView):

    renderer_classes = (JSONRenderer,)
    def get(self,request):
        """
        :param request: 
        :return: All last conversation history of the current user with other users
        """

        convoSender= Conversation.objects.annotate(max_date=Max('messageId__conversation__lastModified')).filter(lastModified=F('max_date'), messageId__sender= request.user.id)
        convoReceiver= Conversation.objects.annotate(max_date=Max('messageId__conversation__lastModified')).filter(lastModified=F('max_date'), messageId__receiver= request.user.id)

        conversations = convoSender | convoReceiver
        serializer = UserConversationSerializer(conversations, many=True)
        return Response(serializer.data)





class UserMetaAPIView(APIView):

    renderer_classes = (JSONRenderer,)
    def get(self,request):
        """
        :param request: 
        :return: All users' images
        """

        userInfo = UserInfo.objects.all()
        serializer = UserInfoSerializer(userInfo, many=True)
        return Response(serializer.data)



