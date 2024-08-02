from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
import json
from django.core.paginator import Paginator
from .models import User, Post, UserNetwork
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def index(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user_author = request.user
            new_post.save()
            messages.success(request, f'Created')
        return redirect(reverse('index'))

    posts = Post.objects.all()
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    allow_to_watch_all = True
    context = {"page_obj": page_obj, 'form': form, 'allow_to_watch_all': allow_to_watch_all}
    return render(request, "network/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def show_user_profile(request, pk):
    author = get_object_or_404(User, pk=pk)
    parent=request.user
    posts = Post.objects.filter(user_author=author)
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    is_this_self_profile = (author == request.user)
    am_i_following = False
    allow_to_watch_all = False
    if not is_this_self_profile:
        try:
            am_i_following = UserNetwork.objects.get(parent=parent, child=author)
        except:
            pass
    context = {'page_obj': page_obj, 'author': author, 'is_this_self_profile': is_this_self_profile,
               'am_i_following': am_i_following, 'allow_to_watch_all': allow_to_watch_all,
               'parent': parent}
    return render(request, 'network/user_profile.html', context)


@login_required(login_url='login')
def show_following(request):
    users_who_i_watch = UserNetwork.objects.filter(parent=request.user)
    i_watch_array= []
    for user in users_who_i_watch:
        i_watch_array.append(user.child.id)
    posts = Post.objects.filter(user_author__in=i_watch_array)
    paginator = Paginator(posts, 10)  # Show 10 posts per page.
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    allow_to_watch_all = True
    context = {'page_obj': page_obj, 'allow_to_watch_all': allow_to_watch_all}
    return render(request, 'network/show_following.html', context)


def toggle_following(request):
    if request.method != "POST":
        return 
    data = json.loads(request.body)
    parent_user = User.objects.get(id=data['parent'])
    child_user = User.objects.get(id=data['child'])
    if data['action'] == 'follow':
        UserNetwork.objects.create(parent=parent_user, child=child_user)
        parent_user.followed_by_user_count = parent_user.followed_by_user_count + 1
        parent_user.save()
        child_user.have_followers_count = child_user.have_followers_count + 1
        child_user.save()
        msg = "followed"
    elif data['action'] == 'unfollow':
        network = UserNetwork.objects.get(parent=parent_user, child=child_user)
        network.delete()
        parent_user.followed_by_user_count = parent_user.followed_by_user_count - 1
        parent_user.save()
        child_user.have_followers_count = child_user.have_followers_count - 1
        child_user.save()
        msg = "unfollowed"
    return JsonResponse({"message": msg, "count": child_user.have_followers_count}, status=201)


def edit_post(request):
    if request.method != "POST":
        return
    data = json.loads(request.body)
    author = get_object_or_404(User, pk=data['user_id'])
    post = get_object_or_404(Post, pk=data['id'])
    if (author != post.user_author):
        return
    post.text = data['text']
    post.save()
    return JsonResponse({"message": 'saved'}, status=201)


def toggle_likes(request):
    if request.method != "POST":
        return
    data = json.loads(request.body)
    user = User.objects.get(id=data['parent'])
    post = get_object_or_404(Post, pk=data['post_id'])
    if data['action'] == 'like':
        post.user_liked_this.add(user)
        post.likes_count = post.likes_count + 1
        post.save()
        msg = "liked"
    elif data['action'] == 'dislike':
        post.user_liked_this.remove(user)
        post.likes_count = post.likes_count - 1
        post.save()
        msg = "disliked"
    
    return JsonResponse({"message": msg, "count": post.likes_count}, status=201)