from django.db import models
class Message(models.Model):
    '''
    the following is the model for the chat message
    fields:
    message: the message text, type: string(max_length=200);
    username: the username of the user who sent the message, 
    type: string(max_length=100), default: 'Anonymous';
    sender: the sender of the message, type: string(max_length=100),
    default: 'Anonymous';
    sendto: the receiver of the message, type: string(max_length=100),
    default: 'Anonymous';
    thread_name: the name of the thread, type: string(max_length=100), 
    not allowed to be null;
    created_at: the time when the message is sent, type: datetime, automatically set;
    '''
    message = models.CharField(max_length=200)
    sender = models.TextField(max_length=100, default='Anonymous')
    sendto = models.TextField(max_length=100, default='Anonymous')
    thread_name = models.CharField(null=True, blank=True, max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.message