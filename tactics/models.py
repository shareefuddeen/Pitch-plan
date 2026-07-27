from django.db import models

class Formation(models.Model):
  name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return self.name

  class Meta:
    ordering = ["-created_at"]



class PlayerPosition(models.Model):
  formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="positions")
  label = models.CharField(max_length=100, blank=True)
  x = models.FloatField()
  y = models.FloatField()


  def __str__(self):
    return f"{self.formation.name} - {self.label or 'player' }"