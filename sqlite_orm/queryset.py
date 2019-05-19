from typing import Any, Dict, Generator, List, Optional, Set, Tuple
from copy import copy

from pypika import Query

from .models import OrmModel
from .fields import Field
from .db_connector import SQLiteClient


class BaseQuery:

    def __init__(self, model) -> None:
        self._joined_tables = []  # type: List[Table]
        self.model = model
        self.query = model._meta.basequery  # type: Query
        self._db = None  # type: Optional[SQLiteClient]
        self.capabilities = model._meta.db.capabilities

    def resolve_ordering(self, model, orderings, annotations) -> None:
        table = Table(model._meta.table)
        for ordering in orderings:
            field_name = ordering[0]
            if field_name not in model._meta.fields:
                raise FieldError(
                    "Unknown field {} for model {}".format(field_name, self.model.__name__)
                )
            self.query = self.query.orderby(getattr(table, ordering[0]), order=ordering[1])


class QuerySet(BaseQuery):

    def __init__(self, model) -> None:
        super().__init__(model)
        self.fields = model._meta.db_fields

        self._get = False  # type: bool
        self._limit = None  # type: Optional[int]
        self._filter_kwargs = {}  # type: Dict[str, Any]
        self._q_objects = []  # type: List[Q]
        self._having = {}  # type: Dict[str, Any]
        self._custom_filters = {}  # type: Dict[str, dict]

    def _clone(self) -> "QuerySet":
        queryset = QuerySet.__new__(QuerySet)
        queryset._db = self._db
        queryset.fields = self.fields
        queryset.model = self.model
        queryset.query = self.query

        queryset._get = self._get
        queryset._limit = self._limit
        queryset._filter_kwargs = copy(self._filter_kwargs)
        queryset._q_objects = copy(self._q_objects)
        queryset._having = copy(self._having)
        queryset._custom_filters = copy(self._custom_filters)
        return queryset

    def _filter_or_exclude(self, *args, negate: bool, **kwargs):
        queryset = self._clone()
        for arg in args:
            if not isinstance(arg, Q):
                raise TypeError("expected Q objects as args")
            if negate:
                queryset._q_objects.append(~arg)
            else:
                queryset._q_objects.append(arg)

        for key, value in kwargs.items():
            if negate:
                queryset._q_objects.append(~Q(**{key: value}))
            else:
                queryset._q_objects.append(Q(**{key: value}))

        return queryset

    def filter(self, *args, **kwargs) -> "QuerySet":
        """
        Filters QuerySet by given kwargs. You can filter by related objects like this:

        .. code-block:: python3

            Team.filter(events__tournament__name='Test')

        You can also pass Q objects to filters as args.
        """
        return self._filter_or_exclude(negate=False, *args, **kwargs)

    def exclude(self, *args, **kwargs) -> "QuerySet":
        """
        Same as .filter(), but with appends all args with NOT
        """
        return self._filter_or_exclude(negate=True, *args, **kwargs)

    def order_by(self, *orderings: str) -> "QuerySet":
        """
        Accept args to filter by in format like this:

        .. code-block:: python3

            .order_by('name', '-tournament__name')

        Supports ordering by related models too.
        """
        queryset = self._clone()
        new_ordering = []
        for ordering in orderings:
            order_type = Order.asc
            if ordering[0] == "-":
                field_name = ordering[1:]
                order_type = Order.desc
            else:
                field_name = ordering

            if not (
                field_name.split("__")[0] in self.model._meta.fields
                or field_name in self._annotations
            ):
                raise FieldError(
                    "Unknown field {} for model {}".format(field_name, self.model.__name__)
                )
            new_ordering.append((field_name, order_type))
        queryset._orderings = new_ordering
        return queryset

    def limit(self, limit: int) -> "QuerySet":
        """
        Limits QuerySet to given length.
        """
        queryset = self._clone()
        queryset._limit = limit
        return queryset

    def all(self) -> "QuerySet":
        """
        Return the whole QuerySet.
        Essentially a no-op except as the only operation.
        """
        return self._clone()

    def first(self) -> "QuerySet":
        """
        Limit queryset to one object and return one object instead of list.
        """
        queryset = self._clone()
        queryset._limit = 1
        queryset._single = True
        return queryset

    def get(self, *args, **kwargs) -> "QuerySet":
        """
        Fetch exactly one object matching the parameters.
        """
        queryset = self.filter(*args, **kwargs)
        queryset._limit = 2
        queryset._get = True
        return queryset

    def _make_query(self) -> Query:
        self.query = self.model._meta.basequery_all_fields
        self.resolve_filters(
            model=self.model,
            q_objects=self._q_objects,
            annotations=self._annotations,
            custom_filters=self._custom_filters,
        )
        if self._limit:
            self.query = self.query.limit(self._limit)
        self.resolve_ordering(self.model, self._orderings, self._annotations)
        return self.query

    def _execute(self):
        instance_list = self._db.executor_class(
            model=self.model,
            db=self._db,
            prefetch_map=self._prefetch_map,
            prefetch_queries=self._prefetch_queries,
        ).execute_select(self.query, custom_fields=list(self._annotations.keys()))
        if not instance_list:
            if self._get:
                raise DoesNotExist("Object does not exist")
            if self._single:
                return None
            return []
        elif self._get:
            if len(instance_list) > 1:
                raise MultipleObjectsReturned("Multiple objects returned, expected exactly one")
            return instance_list[0]
        elif self._single:
            return instance_list[0]
        return instance_list

