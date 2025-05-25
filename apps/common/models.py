import uuid
from django.db import models
from django.utils import timezone

from apps.common.managers import IsDeletedManager, GetOrNoneManager


class BaseModel(models.Model):
    """
    A base model class that includes common fields and methods for all models.

    This abstract model provides common functionality for all models in the application,
    including UUID-based primary keys and timestamp fields for creation and updates.

    Attributes:
        id (UUIDField): Unique identifier for the model instance.
        created_at (DateTimeField): Timestamp when the instance was created.
        updated_at (DateTimeField): Timestamp when the instance was last updated.
    """

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GetOrNoneManager()

    class Meta:
        abstract = True


class IsDeletedModel(BaseModel):
    """
    A model that supports soft deletion functionality.

    This abstract model extends BaseModel to add soft deletion capabilities.
    Instead of permanently deleting records, it marks them as deleted and stores
    the deletion timestamp.

    Attributes:
        is_deleted (BooleanField): Flag indicating if the record is deleted.
        deleted_at (DateTimeField): Timestamp when the record was deleted.
    """

    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    objects = IsDeletedManager()

    def delete(self, *args, **kwargs):
        """
        Perform a soft delete by marking the record as deleted.

        This method overrides the default delete behavior to implement soft deletion.
        Instead of removing the record, it sets is_deleted to True and records the deletion time.
        """
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=["is_deleted", "deleted_at"])

    def hard_delete(self, *args, **kwargs):
        """
        Perform a permanent deletion of the record.

        This method permanently removes the record from the database.
        Use with caution as this operation cannot be undone.
        """
        super().delete(*args, **kwargs)
