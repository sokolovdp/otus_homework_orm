from copy import copy

from pypika import Order, Query, Table

from .exceptions import OrmOperationalError


class QuerySet:

    def __init__(self, model) -> None:
        self.model = model
        self.query = model._meta.basequery
        self._db = None
        self.fields = model._meta.db_fields

        self._get = False
        self._limit = None
        self._filter_kwargs = {}
        self._q_objects = []
        self._having = {}
        self._custom_filters = {}

    def _clone(self):
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

    def resolve_ordering(self, model, orderings) -> None:
        table = Table(model._meta.table)
        for ordering in orderings:
            field_name = ordering[0]
            if field_name in model._meta.fetch_fields:
                raise OrmOperationalError(
                    "Filtering by relation is not possible. Filter by nested field of related model"
                )
            else:
                if field_name not in model._meta.fields:
                    raise OrmOperationalError(
                        "Unknown field {} for model {}".format(field_name, self.model.__name__)
                    )
                self.query = self.query.orderby(getattr(table, ordering[0]), order=ordering[1])

    def order_by(self, *orderings: str):
        queryset = self._clone()
        new_ordering = []
        for ordering in orderings:
            order_type = Order.asc
            if ordering[0] == "-":
                field_name = ordering[1:]
                order_type = Order.desc
            else:
                field_name = ordering
            new_ordering.append((field_name, order_type))
        queryset._orderings = new_ordering
        return queryset

    def limit(self, limit: int):
        """
        Limits QuerySet to given length.
        """
        queryset = self._clone()
        queryset._limit = limit
        return queryset

    def all(self):
        """
        Return the whole QuerySet.
        Essentially a no-op except as the only operation.
        """
        return self._clone()

    def get(self, *args, **kwargs):
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
            custom_filters=self._custom_filters,
        )
        if self._limit:
            self.query = self.query.limit(self._limit)
        self.resolve_ordering(self.model)
        return self.query

    def _execute(self):
        instance_list = self._db.executor_class(
            model=self.model,
            db=self._db,
        ).execute_select(self.query)
        if not instance_list:
            if self._get:
                raise OrmOperationalError("Object does not exist")

            return []
        elif self._get:
            if len(instance_list) > 1:
                raise OrmOperationalError("Multiple objects returned, expected exactly one")
            return instance_list[0]

        return instance_list

