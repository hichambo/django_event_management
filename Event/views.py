from django.shortcuts import render
from requests import Response
from rest_framework import status


# Create your views here.
from rest_framework import viewsets, permissions
from .models import Event, Registration, Ticket, User
from .serializers import EventSerializer, RegistrationSerializer, TicketSerializer, UserSerializer

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Exiger une authentification pour les opérations non GET

    def create(self, request):
        # Valider et enregistrer un nouvel événement
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # Mettre à jour un événement existant
        event = self.get_object()
        serializer = self.get_serializer(instance=event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.IsAuthenticated]  # Exiger une authentification pour toutes les opérations

    def create(self, request):
        # Enregistrer une nouvelle inscription
        event_id = request.data['event']
        event = Event.objects.get(pk=event_id)

        # Vérifier si l'utilisateur est déjà inscrit à cet événement
        if Registration.objects.filter(participant=request.user, event=event).exists():
            return Response({"error": "L'utilisateur est déjà inscrit à cet événement."}, status=status.HTTP_400_BAD_REQUEST)

        # Créer une nouvelle inscription
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        # Mettre à jour une inscription existante
        registration = self.get_object()

        # Vérifier si l'utilisateur est le participant de l'inscription
        if registration.participant != request.user:
            return Response({"error": "Vous n'êtes pas autorisé à modifier cette inscription."}, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance=registration, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]  # Exiger une authentification pour toutes les opérations

    def create(self, request):
        # Créer un nouveau billet
        registration_id = request.data['registration']
        registration = Registration.objects.get(pk=registration_id)

        # Vérifier si l'utilisateur est le participant de l'inscription
        if registration.participant != request.user:
            return Response({"error": "Vous n'êtes pas autorisé à créer un billet pour cette inscription."}, status=status.HTTP_403_FORBIDDEN)

        # Vérifier si l'événement est payant et si le prix est correct
        event = registration.event
        if event.ticket_price is not None and request.data['price'] != event.ticket_price:
            return Response({"error": "Le prix du billet est incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        # Créer un nouveau billet
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # Exiger une
