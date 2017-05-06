app.controller('inboxCtrl',['$scope','$routeParams','$http', function($scope, $routeParams, $http){

    $scope.showConversation = false;

    $scope.init=function(){
        $scope.loadUsers();
        $scope.loadInboxMessages();
        $scope.activeUserId= angular.element($('#userID')).val();
        $scope.mediaUrl= angular.element($('#mediaUrl')).val();
        $scope.inboxList = true;
    }



    //user
    //load all users
    $scope.userList=[];
    $scope.loadUsers = function(){
    $http.get('http://127.0.0.1:8000/chats/api/userInfo').then (function(res){
        $scope.userList=res.data;
        });
    }


    //load user images
    $scope.loadUserImages= function(){
        $http.get('http://127.0.0.1:8000/chats/api/userMeta').then (function(res){
        $scope.userImageList = res.data;

        for(var m in $scope.messageList){
         msgObj = ($scope.messageList[m].messageId.sender.id == $scope.activeUserId || $scope.messageList[m].messageId.receiver.id==$scope.activeUserId)? $scope.messageList[m].messageId : {};

         if(msgObj != {}){
         userId= ($scope.messageList[m].messageId.sender.id == $scope.activeUserId)?$scope.messageList[m].messageId.receiver.id:$scope.messageList[m].messageId.sender.id;
         for(var i in $scope.userImageList){

            if($scope.userImageList[i].userId == userId)
            {
                $scope.messageList[m]['image'] = $scope.mediaUrl + $scope.userImageList[i].image;
            }
         }
         }
        }
    });
        }





    //conversation
    $scope.conversationList= [];

        //load conversation on user select
        $scope.onUserSelect = function(index){
        $scope.anotherUser = $scope.userList[index];
        $scope.showConversation = true;

        //load existing message with receiver user or blank if new message
        $http.get('http://127.0.0.1:8000/chats/api/allMessages',{ params: { userId: $scope.anotherUser.id }}).then (function(res){

        console.log("res data");
        console.log(res.data);
        if(res.data.length>0){
        $scope.existingUserMessageId= res.data[0].id;
        console.log("eumId");
        console.log($scope.existingUserMessageId);

        $http.get('http://127.0.0.1:8000/chats/api/allConversations',{ params: { existingUserMessageId: $scope.existingUserMessageId }}).then (function(res){
        $scope.conversationList = res.data;
        });
        }
        else{
        $scope.existingUserMessageId = "";
        $scope.conversationList = [];
        }
        });
    }


    //on selecting message load conversation
    $scope.onMessageSelect = function(index, existingMessageId, receiver, sender){

        $scope.anotherUser = (receiver==$scope.activeUserId)? ($scope.messageList[index].messageId.sender) : ($scope.messageList[index].messageId.receiver);
        $scope.existingUserMessageId = existingMessageId;

        $http.get('http://127.0.0.1:8000/chats/api/allConversations',{ params: { existingUserMessageId: existingMessageId }}).then (function(res){
        $scope.conversationList = res.data;
        $scope.showConversation = true;
        });
    }



    //message
    //send message
    $scope.sendClicked= function(){

    $scope.messageObj = {};
    $scope.messageObj.receiver= $scope.anotherUser.id;
    if($scope.existingUserMessageId){$scope.messageObj = $scope.existingUserMessageId}


    //new message
    if(!$scope.existingUserMessageId){
    $http.post('http://127.0.0.1:8000/chats/api/sendMessage', $scope.messageObj).then (function(res){

        $scope.conversationObj= {};
        $scope.conversationObj.text= $scope.messageBody;
        $scope.conversationObj.messageId= res.data.id;

        $http.post('http://127.0.0.1:8000/chats/api/allConversations', $scope.conversationObj).then (function(res){
        $scope.loadConversation($scope.conversationObj.messageId);
        });
        });
    }
     //if previous message exits add new conversation for the message
    else{
        $scope.conversationObj= {};
        $scope.conversationObj.text= $scope.messageBody;
        $scope.conversationObj.messageId= $scope.existingUserMessageId;

        $http.post('http://127.0.0.1:8000/chats/api/allConversations', $scope.conversationObj).then (function(res){
        $scope.loadConversation($scope.existingUserMessageId);
        });
    }
    $scope.loadInboxMessages();
 }



    //load conversation after sending message
    $scope.loadConversation = function(existingMessageId) {
        $scope.conversationList = [];
        $http.get('http://127.0.0.1:8000/chats/api/allConversations',{ params: { existingUserMessageId: existingMessageId }}).then (function(res){
        $scope.conversationList = res.data;
        $scope.messageBody = "";
        });
        }



    //message list
    $scope.messageList= [];
    $scope.loadInboxMessages = function(){

        $http.get('http://127.0.0.1:8000/chats/api/userConversation').then (function(res){
            $scope.messageList=res.data;
            console.log("msg list");
            console.log($scope.messageList);
            $scope.loadUserImages();
        });
    }



    //delete message
    $scope.deleteMessage = function(tobeDeletedId){
        $scope.deleteOrArchive = true;
        $scope.showConversation = false;
        $scope.anotherUser = {};

        $http.get('http://127.0.0.1:8000/chats/api/allMessages',{ params: { tobeDeletedId: tobeDeletedId }}).then (function(res){
        $scope.conversationList = res.data;
        $scope.deleteOrArchive = false;
        $scope.loadInboxMessages();
        });
    }



    //archive message
    $scope.archiveMessage = function(tobeArchivedId){
        $scope.deleteOrArchive = true;
        $scope.showConversation = false;
        $scope.anotherUser = {};

        $http.get('http://127.0.0.1:8000/chats/api/allMessages',{ params: { tobeArchivedId: tobeArchivedId }}).then (function(res){
        $scope.conversationList = res.data;
        $scope.deleteOrArchive = false;
        $scope.loadInboxMessages();
        });
    }

    //show archived messages
    $scope.archiveClicked = function(){
        $scope.showConversation = false;
        $scope.inboxList = false;
    }

    //show inbox messages
    $scope.inboxClicked = function(){
        $scope.showConversation = false;
        $scope.inboxList = true;
    }


}]);