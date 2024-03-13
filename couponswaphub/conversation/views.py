from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from coupon.models import Coupon
from .forms import ConversationMessageForm
from .models import Conversation
# Create your views here.

@login_required
def new_conversation(request,coupon_pk):
    coupon = get_object_or_404(Coupon,pk=coupon_pk)

    if coupon.published_by == request.user:
        return redirect('dashboard:index')

    conversation=Conversation.objects.filter(coupon=coupon).filter(members__in=[request.user.id])

    if conversation:
        return redirect('conversation:detail',pk=conversation.first().id)

    if request.method == 'POST':
        form=ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation=Conversation.objects.create(coupon=coupon)
            conversation.members.add(request.user)
            conversation.members.add(coupon.published_by)
            conversation.save()

            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()

            return redirect('coupon:detail', pk=coupon_pk)
    else:
       form=ConversationMessageForm()

    return render(request,'conversation/new.html', {
            'form':form
        })

@login_required
def inbox(request):
    conversations= Conversation.objects.filter(members__in=[request.user.id])

    return render(request,'conversation/inbox.html',{
        'conversations':conversations
    })

@login_required
def detail(request,pk):
    conversation=Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form=ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message=form.save(commit=False)
            conversation_message.conversation=conversation
            conversation_message.created_by=request.user
            conversation_message.save()

            conversation.save()

            return redirect('conversation:detail',pk=pk)
    else:
        form=ConversationMessageForm()

    return render(request,'conversation/detail.html',{
        'conversation':conversation,
        'form':form
    })