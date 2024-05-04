from rest_framework import serializers
from .models import Event, Registration, Ticket, User

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.name', read_only=True)  # Nom de l'organisateur

    class Meta:
        model = Event
        fields = '__all__'  # Inclure tous les champs du modèle Event

class RegistrationSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='event.name', read_only=True)  # Nom de l'événement
    participant_name = serializers.CharField(source='participant.name', read_only=True)  # Nom du participant

    class Meta:
        model = Registration
        fields = '__all__'  # Inclure tous les champs du modèle Registration

class TicketSerializer(serializers.ModelSerializer):
    registration_participant_name = serializers.CharField(source='registration.participant.name', read_only=True)  # Nom du participant lié à l'inscription

    class Meta:
        model = Ticket
        fields = '__all__'  # Inclure tous les champs du modèle Ticket

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'user_type')  # Sélectionner uniquement les champs souhaités pour l'utilisateur

        # Optionnel : exclure le champ password de la sérialisation
        extra_kwargs = {'password': {'write_only': True}}
