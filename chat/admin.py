from django.contrib import admin
from chat.models import Chat, Message

class MessageAdmin(admin.ModelAdmin):    
    fields = ('chat','text','created_at', 'author', 'receiver')    
    list_display = ('created_at', 'author', 'text', 'receiver')    
    search_fields = ('text',)

# Registrieren Sie Ihr Modell mit der MessageAdmin-Klasse
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)

# Register your models here.
