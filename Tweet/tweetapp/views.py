from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Tweet
from .forms import Tweetform

# Display all tweets
def tweet_list(request):
    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'tweet_list.html', {'tweets': tweets})

# Create a new tweet
def tweet_created(request):
    if request.method == "POST":
        form = Tweetform(request.POST, request.FILES)
        
        if form.is_valid():
            tweet = form.save(commit=False)
            
            # Assign a default user (e.g., admin or dummy user)
            default_user = User.objects.first()  # You can customize this
            if default_user:
                tweet.user = default_user  # Assign default user
            else:
                # Handle case where no user exists
                return redirect('tweet_list')

            tweet.save()
            return redirect('tweet_list')
    else:
        form = Tweetform()

    return render(request, 'tweet_form.html', {'form': form})

# Edit an existing tweet
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if request.method == "POST":
        form = Tweetform(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            form.save()
            return redirect('tweet_list')
    else:
        form = Tweetform(instance=tweet)

    return render(request, 'tweet_form.html', {'form': form})

# Delete tweet
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if request.method == "POST":
        tweet.delete()
        return redirect('tweet_list')

    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})
