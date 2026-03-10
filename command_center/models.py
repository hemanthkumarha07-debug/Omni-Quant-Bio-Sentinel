from django.db import models

class SentinelLog(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=50)  # e.g., "STRESS_LOCKDOWN"
    ear_score = models.FloatField()
    market_snapshot = models.JSONField()           # Stores Greeks at time of event
    ai_recommendation = models.TextField()

    class Meta:
        ordering = ['-timestamp']