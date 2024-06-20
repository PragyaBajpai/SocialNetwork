from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from .serializers import UserRegistrationSerializer, FriendRequestSerializer
from django.db.models import Q
from .models import FriendRequest
from datetime import datetime, timedelta


class UserPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = "page_size"
    max_page_size = 100


class SignupView(APIView):
    def post(self, request):
        email = request.data.get("email", "").lower()
        password = request.data.get("password", "")
        username = request.data.get("username", "")
        first_name = request.data.get("first_name", "")
        last_name = request.data.get("last_name", "")

        if not email or not password:
            return Response(
                {"error": "Email and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
            )
            return Response(
                {"message": "User created successfully"}, status=status.HTTP_201_CREATED
            )
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):

        email = request.data.get("email", "").lower()
        password = request.data.get("password", "")

        user = User.objects.filter(email=email).first()
        if user is None or not user.check_password(password):
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_200_OK,
        )


class UserSearchViewSet(APIView):

    pagination_class = UserPagination

    def get(self, request):
        search_keyword = request.query_params.get("search")
        if not search_keyword:
            return Response([])

        paginator = UserPagination()

        # Check : if its a valid email - make validate email
        if "@" in search_keyword:
            users = User.objects.filter(email__iexact=search_keyword)
            result_page = paginator.paginate_queryset(users, request)
            serializer = UserRegistrationSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Check : Search by name
        users = User.objects.filter(
            Q(username__icontains=search_keyword)
            | Q(first_name__icontains=search_keyword)
        )

        result_page = paginator.paginate_queryset(users, request)
        serializer = UserRegistrationSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)


class FriendRequestAPIView(APIView):

    def post(self, request, *args, **kwargs):
        from_user = request.user
        to_user_id = request.data.get("to_user_id")

        # Check if user has sent more than 3 requests in the last minute
        recent_requests = FriendRequest.objects.filter(
            from_user__username=from_user,
            created_at__gte=datetime.now() - timedelta(minutes=1),
        ).count()

        if recent_requests >= 3:
            return Response(
                {"message": "Exceeded the limit of 3 friend requests per minute."},
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )

        # Check if the request is valid
        try:
            to_user = User.objects.get(username=to_user_id)
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid user ID."}, status=status.HTTP_404_NOT_FOUND
            )

        # Check if a request already exists
        existing_request = FriendRequest.objects.filter(
            from_user__username=from_user, to_user=to_user
        ).exists()
        if existing_request:
            return Response(
                {"message": "Friend request already sent."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Create the friend request
        friend_request = FriendRequest(
            from_user=from_user, to_user=to_user, status="pending"
        )
        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request):

        from_user = request.data.get("from_user")
        to_user = request.data.get("to_user")

        action = request.data.get("action")

        if action not in ["accept", "reject"]:
            return Response(
                {"message": 'Invalid action parameter. Use "accept" or "reject".'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        elif not (from_user and to_user):
            return Response(
                {"message": 'Invalid parameter. Send "From User" & "To User".'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        friend_request = FriendRequest.objects.filter(
            from_user__username=from_user, to_user__username=to_user, status="pending"
        ).first()

        if not friend_request:
            return Response(
                {"message": "Friend request not found or already responded."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if action == "accept":
            friend_request.status = "accepted"
        elif action == "reject":
            friend_request.status = "rejected"

        friend_request.save()

        serializer = FriendRequestSerializer(friend_request)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        action = request.query_params.get("action")
        user = request.user

        if action == "list_friends":
            friends = User.objects.filter(
                Q(
                    sent_friend_requests__to_user=user,
                    sent_friend_requests__status="accepted",
                )
                | Q(
                    received_friend_requests__from_user=user,
                    received_friend_requests__status="accepted",
                )
            ).distinct()
            # friends = self.get_friends(request.user)
            serializer = UserRegistrationSerializer(friends, many=True)
            return Response(serializer.data)

        elif action == "list_pending_requests":
            pending_requests = FriendRequest.objects.filter(
                to_user__username=user, status="pending"
            )
            serializer = FriendRequestSerializer(pending_requests, many=True)
            return Response(serializer.data)
        else:
            return Response(
                {"message": "Invalid action parameter."},
                status=status.HTTP_400_BAD_REQUEST,
            )
