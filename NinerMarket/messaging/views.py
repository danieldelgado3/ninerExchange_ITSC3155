from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Conversation, Message
from base.models import Listing

# Create your views here.

@login_required
def conversation_list(request):
    conversations = Conversation.objects.filter(participants=request.user)
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id, participants=request.user)
    messages = conversation.messages.all()
    
    # Mark messages as read
    conversation.messages.filter(is_read=False).exclude(sender=request.user).update(is_read=True)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=content
            )
            return redirect('messaging:conversation_detail', conversation_id=conversation_id)
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages
    })

@login_required
def start_conversation(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    seller = listing.seller  # Making sure Listing model has a seller field
    
    # Checking if conversation already exists
    conversation = Conversation.objects.filter(
        listing=listing,
        participants=request.user
    ).first()
    
    if not conversation:
        conversation = Conversation.objects.create(listing=listing)
        conversation.participants.add(request.user, seller)
    
    return redirect('messaging:conversation_detail', conversation_id=conversation.id)
