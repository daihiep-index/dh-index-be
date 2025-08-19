from dh_index.apps.user.model_container import (
    uuid, models
)
from dh_index.apps.user.models import User


class UserPortfolio(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(null=False, blank=True)
    description = models.TextField(null=False, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "user": self.user,
            "name": self.name,
            "description": self.description,
        }
