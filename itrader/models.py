from django.db import models
from django.conf import settings

class StockData(models.Model):
    security = models.CharField(max_length=20, unique=True)
    lastprice= models.IntegerField()
    demandqty= models.IntegerField()
    demandprice= models.IntegerField()
    supplyprice= models.IntegerField()
    supplyqty= models.IntegerField()
    lastqty= models.IntegerField()
    high= models.IntegerField()
    low= models.IntegerField()

class Message(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.CharField(max_length=255)
    content = models.TextField()
    date_added = models.DateTimeField()

    class Meta:
        ordering = ('date_added',)

class Room(models.Model):
    # title = models.CharField(max_length=255, unique=True, blank=False,)
    title = models.ForeignKey(StockData, on_delete=models.CASCADE)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, help_text="users who are connected to the chat")

    def __str__(self):
        return self.title
    def connect_user(self,user):
        # return true if user is added to the list
        is_user_added = False
        if not user in self.users.all():
            self.users.add(user)
            self.save()
            is_user_added = True
        elif user in self.users.all():
            is_user_added = True
        return is_user_added
    def disconnect_user(self, user):
        # retur true if user is removed from the user list
        is_user_removed = False
        if not user in self.users.all():
            self.users.remove(user)
            self.save()
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        # returns the channel name that sockets should subscribe to and get sent messages as they are generated
        return f"PublicChatRoom-{self.id}"



class Trade(models.Model):
    clientcode = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    buysell =  models.CharField(max_length=20)
    security =  models.ForeignKey(StockData, on_delete=models.CASCADE)
    market =  models.CharField(max_length=20)
    quantity =  models.IntegerField()
    price =  models.IntegerField()
    validupto =  models.DateField()
    delivery = models.CharField(max_length=20)
    dateplaced = models.DateTimeField(auto_now_add=True)

# def get_default_category():
#     # get_or_create returns a tuple and we will only need the first value, which is the object
#     return Package_Category.objects.get_or_create(name="Free")[0]

# package_category = models.ForeignKey(Package_Category, on_delete=models.DO_NOTHING, verbose_name="Package Category", null=True, default=get_default_category)


# class PublicRoomChatMessageManager(models.Manager):
#     def by_room(self,room):
#         #return new messages first
#         qs = PublicRoomChatMessage.object.filter(room=room).order_by("-timestamp")
#         return qs

# class PublicRoomChatMessage(models.Model):
#     # Chat message created by user inside a PublicChatRoom
#     username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     room = models.ForeignKey(PublicChatRoom, on_delete=models.CASCADE)
#     timestamp = models.DateTimeField(auto_now_add = True)
#     content = models.TextField(unique=False, blank=False)

#     objects =PublicRoomChatMessageManager()

#     class Meta:
#         ordering = ('timestamp',)
