from pypika import Query

from . import fields, db_connector, exceptions


class ModelInfo:

    def __init__(self, meta):
        self.table = getattr(meta, "table", "")
        self.fields = set()
        self.fields_map = dict()
        self.db_connection = None
        self.base_query = Query
        self._inited = None

    @property
    def db(self):
        if db_connector.ORM.current_connection:
            return db_connector.ORM.current_connection
        else:
            raise exceptions.OrmOperationalError("No DB associated to model")


class ModelMeta(type):
    __slots__ = ()

    def __new__(mcs, name: str, bases, attrs: dict):
        fields_map = dict()

        # if "id" not in attrs:
        #     attrs["id"] = fields.IntegerField(is_pk=True)

        for key, value in attrs.items():
            if isinstance(value, fields.Field):
                fields_map[key] = value
                if not value.db_field_name:
                    value.db_field_name = key

        meta = ModelInfo(attrs.get("Meta"))
        meta.fields_map = fields_map
        meta.fields = set(fields_map.keys())
        meta.db_connection = None
        meta._inited = False
        attrs["_meta"] = meta

        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class


class OrmModel(metaclass=ModelMeta):
    _meta = ModelInfo(None)

    # id = None

    def __init__(self, **kwargs):
        meta = self._meta
        for key, value in kwargs.items():
            if key in meta.fields:
                field_object = meta.fields_map[key]
                if value is None and not field_object.nullable:
                    raise exceptions.OrmConfigurationError(f"{key} is non nullable field, but null was passed")
                field_object.value = value

    @classmethod
    def create(self, **kwargs):
        self.__init__(**kwargs)

    def update(self, **kwargs):
        pass

    def save_to_db(self, **kwargs):
        # if self.id is not None:
        #     self.update(**kwargs)
        # else:
        #     self.insert(**kwargs)
        pass

    def delete_from_db(self):
        db = self._meta.db_connection
        # if self.id.value is None:
        #     raise exceptions.OrmOperationalError("Can't delete uncreated record")
        # db.execute_delete(table=self)

    def asdict(self):
        return {name: field.value for name, field in self._meta.fields_map.items()}
