from django.db import models
from django.utils import timezone


class GetOrNoneQuerySet(models.QuerySet):
    """
    Custom QuerySet that adds get_or_none functionality.

    This QuerySet extends Django's default QuerySet to provide a get_or_none method,
    which returns None instead of raising an exception when no object is found.

    Methods:
        get_or_none: Returns an object matching the given lookup parameters or None.
    """

    def get_or_none(self, **kwargs):
        """
        Get a single object matching the given lookup parameters or return None.

        Args:
            **kwargs: Lookup parameters to filter the queryset.

        Returns:
            Model instance or None: The matching object if found, None otherwise.
        """
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class GetOrNoneManager(models.Manager):
    """
    Manager that adds get_or_none functionality to model objects.

    This manager extends Django's default manager to provide a get_or_none method
    through a custom QuerySet.

    Methods:
        get_queryset: Returns a GetOrNoneQuerySet instance.
        get_or_none: Returns an object matching the given lookup parameters or None.
    """

    def get_queryset(self):
        """
        Return a GetOrNoneQuerySet instance.

        Returns:
            GetOrNoneQuerySet: A queryset with get_or_none functionality.
        """
        return GetOrNoneQuerySet(self.model)

    def get_or_none(self, **kwargs):
        """
        Get a single object matching the given lookup parameters or return None.

        Args:
            **kwargs: Lookup parameters to filter the queryset.

        Returns:
            Model instance or None: The matching object if found, None otherwise.
        """
        return self.get_queryset().get_or_none(**kwargs)


class IsDeletedQuerySet(GetOrNoneQuerySet):
    """
    QuerySet that supports soft deletion functionality.

    This QuerySet extends GetOrNoneQuerySet to add soft deletion capabilities.
    It provides methods for both soft and hard deletion of records.

    Methods:
        delete: Performs soft deletion by default, with option for hard deletion.
    """

    def delete(self, hard_delete=False):
        """
        Delete the queryset, either softly or permanently.

        Args:
            hard_delete (bool): If True, performs permanent deletion.
                               If False (default), performs soft deletion.

        Returns:
            tuple: (number of deleted objects, dict with number of deletions per object type)
        """
        if hard_delete:
            return super().delete()
        else:
            return self.update(is_deleted=True, deleted_at=timezone.now())


class IsDeletedManager(GetOrNoneManager):
    """
    Manager that supports soft deletion functionality.

    This manager extends GetOrNoneManager to add soft deletion capabilities.
    It provides filtered querysets that exclude soft-deleted records by default.

    Methods:
        get_queryset: Returns a filtered queryset excluding soft-deleted records.
        unfiltered: Returns an unfiltered queryset including soft-deleted records.
        hard_delete: Performs permanent deletion of records.
    """

    def get_queryset(self):
        """
        Return a queryset excluding soft-deleted records.

        Returns:
            IsDeletedQuerySet: A queryset filtered to exclude soft-deleted records.
        """
        return IsDeletedQuerySet(self.model).filter(is_deleted=False)

    def unfiltered(self):
        """
        Return an unfiltered queryset including soft-deleted records.

        Returns:
            IsDeletedQuerySet: An unfiltered queryset including all records.
        """
        return IsDeletedQuerySet(self.model)

    def hard_delete(self):
        """
        Perform permanent deletion of records.

        Returns:
            tuple: (number of deleted objects, dict with number of deletions per object type)
        """
        return self.unfiltered().delete(hard_delete=True)
