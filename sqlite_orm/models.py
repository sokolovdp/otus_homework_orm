import sqlite_orm
from sqlite_orm import exceptions, fields

ALL_ORM_TABLES = []


class ModelInfo:

    def __init__(self, meta):
        self.db_table = getattr(meta, "db_table", None)
        self.safe_create = getattr(meta, "safe_create", False)
        self.fields = None
        self.fields_map = None
        self.fields_db = None
        self.started = None
        self.db_client = None
        self.basequery = None


class ModelMeta(type):

    def __new__(mcs, name, bases, attrs):
        global ALL_ORM_TABLES
        fields_map = dict()
        fields_db = dict()
        fk_fields = set()

        if "id" not in attrs:
            attrs["id"] = fields.IntegerField(is_pk=True)

        for name, field in attrs.items():
            if isinstance(field, fields.Field):
                fields_map[name] = field
                field.model_field_name = name
                if isinstance(field, fields.ForeignKeyField):
                    key_field = "{}_id".format(name)
                    field.source_name = name
                    fields_db[key_field] = key_field
                    fields_map[key_field] = fields.IntegerField(
                        reference=field,
                        nullable=field.nullable,
                        default=field.default
                    )
                    fk_fields.add(name)
                else:
                    if not field.db_field_name:
                        field.db_field_name = name
                    fields_db[name] = field.db_field_name

        meta = ModelInfo(attrs.get("Meta"))
        meta.fields_map = fields_map
        meta.fields = set(fields_map.keys())
        meta.fields_db = fields_db
        meta.fk_fields = fk_fields
        meta.db_client = None
        attrs["model_meta"] = meta

        new_class = super().__new__(mcs, name, bases, attrs)
        ALL_ORM_TABLES.append(new_class)
        return new_class


class OrmModel(metaclass=ModelMeta):
    model_meta = ModelInfo(None)
    id = None

    def __init__(self, **kwargs):
        meta = self.model_meta
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

    def __str__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __repr__(self) -> str:
        if self.id:
            return f"<{self.__class__.__name__}: {self.id}>"
        return f"<{self.__class__.__name__}>"

    def __hash__(self) -> int:
        if not self.id:
            raise TypeError("Model instance without ID is not hashable")
        return hash(self.__repr__())

    def __eq__(self, other) -> bool:
        return hash(self) == hash(other)

    def as_dict(self):
        return self.__dict__

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        instance.save(**kwargs)
        return instance

    def _update(self, instance, **kwargs):
        instance.model_meta.db_client.execute_update(instance, **kwargs)

    def _insert(self, instance, **kwargs):
        instance.model_meta.db_client.execute_insert(instance, **kwargs)

    def save(self, **kwargs):
        if self.id is not None:
            self._update(self, **kwargs)
        else:
            self._insert(self, **kwargs)

    def delete(self):
        if self.id is None:
            raise exceptions.OrmOperationalError("Can't delete uncreated record")
        else:
            return self.model_meta.db_client.execute_delete(self)

    @classmethod
    def select(cls, *args, **kwargs):
        return cls.model_meta.db_client.execute_select(cls, *args, **kwargs)


