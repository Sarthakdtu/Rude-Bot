from django.shortcuts import render, redirect
import requests
import random
from chatter.models import Chat, UserMessage, BotMessage, User
# Create your views here.

def bot_reply(msg, username):
    words = list(msg.split(" "))
    name=""
    tool=""
    thing=""
    insults=["back/"+username, "asshole", "bag", "bucket",
    "chainsaw/"+username, "donut/"+username, "family", "fyyff",
    "keep/"+username,"king/"+username,"nugget/"+username]
    insult_others=["ballmer/"+name+"/"+name]
    greetings=["bday/"+username, "/awesome", "bm/"+username, "mornin", "off/"+username, "outside/"+username]
    reaction=""
    question_answer=["because"]
    calm=["keepcalm/"+reaction]
    bye=["bye"]
    dont_care=["give", "immensity", "look/"+username, "looking", "no"]
    use_something=["caniuse/"+tool]
    do_something=["dosomething/do/"+thing]
    story=["cool", "cup", "flying", "fascinating"]
    everyone = ["everything", "everyone", "fts"]

    if len(words)>50:
        return random.choice(story)
    if "story" in words:
        return random.choice(story)
    if "Why?" in words:
        return random.choice(question_answer)
    return random.choice(insults)




def chat(request, username):
    #chats = Chat.objects.filter(user=username).values("bot_messages__text", "user_messages__text")
    #chats=list(chats)
    user = User.objects.get(user=username)
    print("faded")
    if request.method=="POST":
        user_msg = request.POST.get("msg", False)
        if user_msg=="":
            redirect('chatter/error.html')
        url_add=bot_reply(user_msg, username)
        url = "http://www.foaas.com/"+url_add+"/bot"
        response = requests.get(url, headers={"Accept":"application/json"}).json()
        message = response["message"]
        print(message)
        b = BotMessage.objects.create(text=message, user=user)
        #BotMessage.save_text()
        u = UserMessage.objects.create(text=user_msg, user=user)
        #UserMessage.save_text()
        Chat.objects.create(user_messages=u, user=user, bot_messages=b);
        print("here")
    print("actually here")
    chats = Chat.objects.filter(user=user).values("bot_messages__text", "user_messages__text")
    chats = list(chats)
    chat_list = []
    for texts in chats:
        b = texts["bot_messages__text"]
        u = texts["user_messages__text"]
        print(b, u)
        chat_list.append((b, u))
    print(chat_list)
    return render(request, "chatter/chat.html", {"messages":chat_list, "user":username})

def error(request):
    return render(request, 'chatter/error.html')

def home(request):
    if request.method == 'POST':
        username = request.POST["username"]
        user, created = User.objects.get_or_create(user=username)
        url = "http://www.foaas.com/blackadder/"+username+"/bot"
        #User.save_user()
        if created:
                    response = requests.get(url, headers={"Accept":"application/json"}).json()
                    message = response["message"]
                    b = BotMessage.objects.create(text=message, user=user)
                    #BotMessage.save_text()
                    u = UserMessage.objects.create(text="", user=user)
                    #UserMessage.save_text()
                    Chat.objects.create(user_messages=u, user=user, bot_messages=b);

        return redirect('chat/'+username)
    else:
        return render(request, 'chatter/home.html', {"user": None})
