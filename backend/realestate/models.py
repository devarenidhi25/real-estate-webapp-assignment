from django.db import models


class RealEstateData(models.Model):
    """
    Model to store real estate data.
    Replaces Excel-based data loading with Django ORM.
    """
    area = models.CharField(max_length=255, db_index=True)
    year = models.IntegerField(db_index=True)
    price = models.FloatField()
    demand = models.IntegerField()

    class Meta:
        indexes = [
            models.Index(fields=['area', 'year']),
        ]
        verbose_name = "Real Estate Data"
        verbose_name_plural = "Real Estate Data"

    def __str__(self):
        return f"{self.area} - {self.year} (₹{self.price:,.0f})"


class QueryLog(models.Model):
    """
    Model to log user queries to the /api/query/ endpoint.
    """
    query_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Query Log"
        verbose_name_plural = "Query Logs"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.query_text[:50]}... ({self.created_at})"
