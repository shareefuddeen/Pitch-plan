from django.db import models

class Formation(models.Model):
  name = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  ball_x = models.FloatField(null=True, blank=True)
  ball_y = models.FloatField(null=True, blank=True)


  
  def __str__(self):
    return self.name

  class Meta:
    ordering = ["-created_at"]



class PlayerPosition(models.Model):

  TEAM_CHOICES = [
    ("home", "Home"),
    ("away", "Away"),
  ]

  
  formation = models.ForeignKey(Formation, on_delete=models.CASCADE, related_name="positions")
  label = models.CharField(max_length=100, blank=True)
  x = models.FloatField()
  y = models.FloatField()
  team = models.CharField(max_length=4, choices=TEAM_CHOICES, default="home")
  


  def __str__(self):
    return f"{self.formation.name} - {self.team} - {self.label or 'player' }"


class MovementArrow(models.Model):
    formation = models.ForeignKey(
        Formation,
        related_name='arrows',
        on_delete=models.CASCADE
    )
    start_x = models.FloatField()
    start_y = models.FloatField()
    end_x = models.FloatField()
    end_y = models.FloatField()

    def __str__(self):
        return f"{self.formation.name} - arrow"