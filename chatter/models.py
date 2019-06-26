from django.db import models

# Create your models here.


class User(models.Model):
    user = models.CharField(max_length=200)
    def save_user(self):
        self.save()

class BotMessage(models.Model):
    text= models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def save_text(self):
        self.save()


class UserMessage(models.Model):
    text= models.TextField()
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def save_text(self):
        self.save()

class Chat(models.Model):
    user_messages = models.ForeignKey("UserMessage", on_delete=models.CASCADE)
    bot_messages = models.ForeignKey("BotMessage", on_delete=models.CASCADE)
    user = models.ForeignKey("User", on_delete=models.CASCADE)

    def save_chat(self):
        self.save()
