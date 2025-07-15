from dh_index.apps.user.model_container import (
    uuid, models
)
from dh_index.apps.user.models import User


class UserHoldings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    stock_code = models.CharField(null=False, blank=True)
    quantity = models.FloatField(null=False, blank=True)
    value = models.FloatField(null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "stock_code": self.stock_code,
            "quantity": self.quantity,
            "value": self.value,
            "total_value": self.quantity * self.value * 1000,
        }
