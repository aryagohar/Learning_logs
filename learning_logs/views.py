from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.db.models import Q
from django.http import Http404
from .models import Topic, Entry
from .forms import TopicForm, EntryForm, DeleteTopicForm

# Create your views here.
def index(request):
    """The home page for Learning Log."""
    return render(request, 'learning_logs/index.html')

@login_required
def topics(request):
    """Show all topics"""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id):
    """Show a single topic and all its entries."""
    topic = Topic.objects.get(id=topic_id)
    # If the topic is public is shown to everyone, otherwise only to its creator.
    if not topic.is_public:
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if topic.owner != request.user:
            raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)

@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = TopicForm()
    else:
        # POST data submitted; process data.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')

    # Display a blank or invalid form.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = EntryForm()
    else:
        # POST data submitted; process data.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Display a blank or invalid form.
    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    if request.method != 'POST':
        # Initial request; pre-fill form with the current entry
        form = EntryForm(instance=entry)
    else:
        # POST data submitted; process data.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)

    # Display a blank or invalid form.
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)

@login_required
def delete_topic(request, topic_id):
    """Delete a topic after password confirmation."""
    topic = get_object_or_404(Topic, id=topic_id)

    # Ensure the topic belongs to the current user
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Show blank password confirmation form
        form = DeleteTopicForm()
    else:
        form = DeleteTopicForm(data=request.POST)
        if form.is_valid():
            entered_password = form.cleaned_data['password']
            # authenticate() hashes entered_password and compares — never raw comparison
            user = authenticate(username=request.user.username, password=entered_password)
            if user is not None:
                # Password correct — delete topic and redirect
                topic.delete()
                return redirect('learning_logs:topics')
            else:
                # Password wrong — add error to form manually
                form.add_error('password', 'Incorrect password. Topic was not deleted.')

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/delete_topic.html', context)


def search(request):
    """Search for topics or entries"""
    query = request.GET.get("q", "")
    if request.user.is_authenticated:
        topics = Topic.objects.filter(
      Q(is_public=True) | Q(owner=request.user),
            text__icontains=query
        )
    else:
        topics = Topic.objects.filter(
            is_public=True,
            text__icontains=query
        )
    if request.user.is_authenticated:
        entries = Entry.objects.filter(
            Q(topic__is_public=True) | Q(topic__owner=request.user),
            text__icontains=query
        )
    else:
        entries = Entry.objects.filter(
            topic__is_public=True,
            text__icontains=query
        )
    context = {
        "topics": topics,
        "entries": entries,
    }
    return render(request, "learning_logs/search.html", context)
