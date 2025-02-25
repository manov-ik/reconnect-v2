from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User, Group
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import UserGroup, Message, Event, CustomUser, GroupUser

User = get_user_model()

@csrf_exempt
def signup(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")
            ph_no = data.get("ph_no")
            roll_no = data.get("roll_no")
            dept = data.get("dept")

            if User.objects.filter(username=username).exists():
                return JsonResponse({"error": "Username already taken"}, status=400)

            # Create user with additional fields
            user = User.objects.create_user(
                username=username,
                password=password,
                ph_no=ph_no,
                roll_no=roll_no,
                dept=dept
            )
            user.save()

            return JsonResponse({"message": "Signup successful!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def user_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(username=username, password=password)  # ✅ Checks encrypted password
            if user:
                login(request, user)
                return JsonResponse({"message": "Login successful!"}, status=200)
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"}, status=200)

@login_required
def get_groups(request):
    try:
        # Get only the groups that the current user belongs to
        user_groups = request.user.groups.all()
        print("Found user groups:", user_groups)  # Debug print
        
        # Convert to list of dictionaries with required fields
        groups_data = list(user_groups.values('id', 'name'))
        print("Groups data:", groups_data)  # Debug print
        
        return JsonResponse(groups_data, safe=False)
    except Exception as e:
        print("Error in get_groups:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def messages(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            sender = get_object_or_404(User, id=data.get("sender_id"))
            receiver_id = data.get("receiver_id")
            group_id = data.get("group_id")
            content = data.get("content")
            media_url = data.get("media_url", "")

            if receiver_id:
                receiver = get_object_or_404(User, id=receiver_id)
                msg = Message.objects.create(sender=sender, receiver=receiver, content=content, media_url=media_url)
            elif group_id:
                group = get_object_or_404(UserGroup, id=group_id)
                msg = Message.objects.create(sender=sender, grp=group, content=content, media_url=media_url)
            else:
                return JsonResponse({"error": "Specify receiver_id or group_id"}, status=400)

            return JsonResponse({"message": "Message sent!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":  # Fetch messages
        messages = Message.objects.all().values("id", "sender__username", "receiver__username", "group__name", "content", "media_url", "timestamp")
        return JsonResponse(list(messages), safe=False)


@csrf_exempt
def events(request):
    if request.method == "POST":  # Create event
        try:
            data = json.loads(request.body)
            name = data.get("name")
            media_url = data.get("media_url", "")
            description = data.get("description")
            registration_link = data.get("registration_link", "")
            posted_by = get_object_or_404(CustomUser, id=data.get("posted_by_id"))

            event = Event.objects.create(
                event_name=name,
                media_url=media_url, 
                event_description=description,
                event_reg_link=registration_link,
                posted_by=posted_by
            )
            return JsonResponse({"message": "Event created!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":  # Fetch events
        events = Event.objects.all().values(
            "id", 
            "event_name",
            "media_url",
            "event_description", 
            "event_reg_link",
            "posted_by__username"
        )
        return JsonResponse(list(events), safe=False)

@csrf_exempt
def group_operations(request):
    if request.method == "GET":
        groups = UserGroup.objects.all().values("id", "name")
        return JsonResponse(list(groups), safe=False)
    
    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get("name")
            
            if not name:
                return JsonResponse({"error": "Name is required"}, status=400)
                
            group = UserGroup.objects.create(name=name)
            
            # If user_id is provided, add them to the group
            user_id = data.get("user_id")
            if user_id:
                user = get_object_or_404(CustomUser, id=user_id)
                GroupUser.objects.create(
                    grp=group,
                    user=user,
                    role="admin"  # First user is admin
                )
            
            return JsonResponse({
                "message": "Group created successfully",
                "group_id": group.id,
                "name": group.name
            }, status=201)
            
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Method not allowed"}, status=405)