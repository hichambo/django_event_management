from django.db import models

# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    event_datetime = models.DateTimeField()
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey('User', on_delete=models.CASCADE, related_name='organized_events')
    category = models.CharField(max_length=50)
    max_capacity = models.IntegerField(null=True, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    event_image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Brouillon'), ('published', 'Publié'), ('cancelled', 'Annulé')])

    def __str__(self):
        return self.name

class Registration(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE)
    participant = models.ForeignKey('User', on_delete=models.CASCADE, related_name='registrations')
    status = models.CharField(max_length=20, choices=[('pending', 'En attente'), ('confirmed', 'Confirmé'), ('cancelled', 'Annulé')])

    def __str__(self):
        return f"{self.participant.name} - {self.event.name}"

class Ticket(models.Model):
    registration = models.ForeignKey('Registration', on_delete=models.CASCADE)
    ticket_type = models.CharField(max_length=20, choices=[('free', 'Gratuit'), ('paid', 'Payant')])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    qr_code = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.registration.participant.name} - {self.ticket_type}"

class User(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hash du mot de passe
    user_type = models.CharField(max_length=20, choices=[('organizer', 'Organisateur'), ('participant', 'Participant')])

    def __str__(self):
        return self.name
