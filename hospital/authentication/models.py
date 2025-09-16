from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Patient(models.Model):
    GENDER_CHOICES = [('m','Male'),('f','Female'),('o','Other')]
    RELATION_CHOICES = [
        ('self','Self'),('spouse','Spouse'),('father','Father'),('mother','Mother'),
        ('son','Son'),('daughter','Daughter'),('brother','Brother'),('sister','Sister'),
        ('grandfather','Grandfather'),('grandmother','Grandmother'),('uncle','Uncle'),
        ('aunt','Aunt'),('cousin','Cousin'),('nephew','Nephew'),('niece','Niece'),
        ('friend','Friend'),('other','Other')
    ]

    name = models.CharField(max_length=200)
    dob = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="patients")
    relation = models.CharField(max_length=20, choices=RELATION_CHOICES)

    def clean(self):
        super().clean()
        if self.user and self.relation in ['self','father','mother']:
            existing = Patient.objects.filter(user=self.user, relation=self.relation)
            if self.pk:
                existing = existing.exclude(pk=self.pk)
            if existing.exists():
                raise ValidationError(f"You can only have one {self.relation} per user.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.get_relation_display()})"
