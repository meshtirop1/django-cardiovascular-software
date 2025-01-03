from django.db import models
import json

class PredictionHistory(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    input_data = models.TextField()  # Replace JSONField with TextField
    prediction = models.CharField(max_length=255)
    confidence_scores = models.TextField()  # Replace JSONField with TextField
    created_at = models.DateTimeField(auto_now_add=True)

    def set_input_data(self, data):
        self.input_data = json.dumps(data)

    def get_input_data(self):
        return json.loads(self.input_data)

    def set_confidence_scores(self, scores):
        self.confidence_scores = json.dumps(scores)

    def get_confidence_scores(self):
        return json.loads(self.confidence_scores)
