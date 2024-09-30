from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from kittymart.filters import KittenFilter
from kittymart.models import Kitten, Rating
from kittymart.serializers import KittenSerializer, UserRegistrationSerializer, RatingSerializer


class KittenViewSet(viewsets.ModelViewSet):
    queryset = Kitten.objects.all()
    serializer_class = KittenSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['description', 'color']
    ordering_fields = ['age_in_months']
    permission_classes = [IsAuthenticated, ]
    filterset_class = KittenFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        kitten = self.get_object()
        if kitten.user != request.user:
            return Response({'detail': 'You do not have permission to edit this kitten.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        kitten = self.get_object()
        if kitten.user != request.user:
            return Response({'detail': 'You do not have permission to edit this kitten.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        kitten = self.get_object()
        if kitten.user != request.user:
            return Response({'detail': 'You do not have permission to delete this kitten.'},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def create_rating(self, request, pk=None):
        kitten = self.get_object()
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(kitten=kitten, user=request.user)  # Устанавливаем котенка и пользователя
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

    # Метод для получения всех оценок котенка
    def get_ratings(self, request, pk=None):
        kitten = self.get_object()
        ratings = kitten.ratings.all()
        serializer = RatingSerializer(ratings, many=True)
        return Response(serializer.data)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "username": user.username,
                "email": user.email,
            }
        }, status=status.HTTP_201_CREATED)




class UserRatingsView(generics.ListAPIView):
    serializer_class = RatingSerializer

    def get_queryset(self):
        return Rating.objects.filter(user=self.request.user)