from django.shortcuts import render

# Create your views here.
class CreateThread(View):
  def get(self, request, *args, **kwargs):
    form = ThreadForm()
    context = {
      'form': form
    }
    return render(request, 'social/create_thread.html', context)
  def post(self, request, *args, **kwargs):
    form = ThreadForm(request.POST)
    username = request.POST.get('username')
    try:
      receiver = User.objects.get(username=username)
      if ThreadModel.objects.filter(user=request.user, receiver=receiver).exists():
        thread = ThreadModel.objects.filter(user=request.user, receiver=receiver)[0]
        return redirect('thread', pk=thread.pk)
      
      if form.is_valid():
        sender_thread = ThreadModel(
          user=request.user,
          receiver=receiver
        )
        sender_thread.save()
        thread_pk = sender_thread.pk
        return redirect('thread', pk=thread_pk)
    except:
      return redirect('create-thread')


class ListThreads(View):
  def get(self, request, *args, **kwargs):
  threads = ThreadModel.objects.filter(Q(user=request.user) | Q(receiver=request.user))
  context = {
    'threads': threads
  }
  return render(request, 'social/inbox.html', context)


class CreateMessage(View):
  def post(self, request, pk, *args, **kwargs):
    thread = ThreadModel.objects.get(pk=pk)
    if thread.receiver == request.user:
      receiver = thread.user
    else:
      receiver = thread.receiver
      message = MessageModel(
        thread=thread,
        sender_user=request.user,
        receiver_user=receiver,
        body=request.POST.get('message'),
      )
      message.save()
      return redirect('thread', pk=pk)



class ThreadView(View):
  def get(self, request, pk, *args, **kwargs):
    form = MessageForm()
    thread = ThreadModel.objects.get(pk=pk)
    message_list = MessageModel.objects.filter(thread__pk__contains=pk)
    context = {
      'thread': thread,
      'form': form,
      'message_list': message_list
    }
    return render(request, 'social/thread.html', context)