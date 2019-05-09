import sqlite_orm
from sqlite_orm import exceptions, fields


class ModelInfo:

    def __init__(self, meta):
        self.db_table_name = getattr(meta, "table", None)
        self.fields = None
        self.fields_map = None
        self.fields_db = None
        self.started = None
        self.db_connection = None

    @property
    def db(self):
        if self.db_connection:
            return self.db_connection
        else:
            raise exceptions.OrmOperationalError("No DB associated to model")


class ModelMeta(type):

    def __new__(mcs, name, bases, attrs):
        fields_map = dict()
        fields_db = dict()

        for name, field in attrs.items():
            if isinstance(field, fields.Field):
                fields_map[name] = field
                if not field.db_field_name:
                    field.db_field_name = name
                fields_db[name] = field.db_field_name

        meta = ModelInfo(attrs.get("Meta"))
        meta.fields_map = fields_map
        meta.fields = set(fields_map.keys())
        meta.fields_db = fields_db
        meta.db_connection = None
        meta.started = False
        attrs["_meta"] = meta

        new_class = super().__new__(mcs, name, bases, attrs)
        return new_class


class OrmModel(metaclass=ModelMeta):
    _meta = ModelInfo(None)

    def __init__(self, **kwargs):
        meta = self._meta
        initiated_fields = set()
        for key, value in kwargs.items():
            if key in meta.fields:
                field_object = meta.fields_map[key]
                if value is None and not field_object.nullable:
                    raise exceptions.OrmConfigurationError(f"{key} is non nullable field, but null was passed")
                setattr(self, key, value)
                initiated_fields.add(key)
        not_initiated_fields = meta.fields - initiated_fields
        for name in not_initiated_fields:
            field_object = meta.fields_map[name]
            if field_object.default:
                setattr(self, name, field_object.default)
            elif field_object.is_pk or not field_object.nullable:
                setattr(self, name, None)
            else:
                raise exceptions.OrmConfigurationError(f"{name} is non nullable field, but no default value set")

        sqlite_orm.ORM.register_model(self)

    def create(self, **kwargs):
        self.__init__(**kwargs)

    def update(self, **kwargs):
        pass

    def save(self, **kwargs):
        # if self.id is not None:
        #     self.update(**kwargs)
        # else:
        #     self.insert(**kwargs)
        pass

    def delete(self):
        db = self._meta.db_connection
        # if self.id.value is None:
        #     raise exceptions.OrmOperationalError("Can't delete uncreated record")
        # db.execute_delete(db_table_name=self)

    def asdict(self):
        return self.__dict__
