from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
# Create your models here.

class Car(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
      


class reservation (models.Model):
  car = models.ForeignKey(Car, on_delete=models.CASCADE)
  from_date = models.DateField()
  to_date = models.DateField()
  note = models.TextField(blank=True, editable=True)
  created_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.car} just got reserved from {self.from_date} to {self.to_date}" 
  
  def check_overlap(self):
        # Check if the reservation overlaps with existing reservations for the same car
        overlapping_reservations = reservation.objects.filter(
            car=self.car,
            from_date__lt=self.to_date,
            to_date__gt=self.from_date
        ).exclude(pk=self.pk if self else None)  # Exclude current instance if updating

        if self and self.pk:
                overlapping_reservations = overlapping_reservations.exclude(pk=self.pk)
                
        return list(overlapping_reservations)
    
  def clean(self):    
        # Call check_overlap and raise ValidationError if overlaps exist
        if not self.from_date or not self.to_date:
                raise ValidationError('Both from_date and to_date are required.')

        if self.from_date > self.to_date:
            raise ValidationError('from_date cannot be later than to_date.')
        
        overlapping_reservations = self.check_overlap()
        if overlapping_reservations:
            overlap_details = format_html('<br>'.join([
                f'ID {res.pk}: makina {res.car} nga data {res.from_date} deri {res.to_date}'
                for res in overlapping_reservations
            ]))
            raise ValidationError(
                format_html('Ke tashme rezervim qe bie ndesh me datat e zgjedhura:<br>{}', overlap_details)
            )
            


  class Meta:
        # Optionally, you can define unique_together here as well for database-level enforcement
        unique_together = ('car', 'from_date', 'to_date')
        ordering = ['-from_date']