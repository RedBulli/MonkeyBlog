from factory import Factory

from MonkeyBook.extensions import db


class SQLAlchemyModelFactory(Factory):
    """
    Factory for SQLAlchemy models.
    """

    ABSTRACT_FACTORY = True

    @classmethod
    def _create(cls, target_class, *args, **kwargs):
        """Create an instance of the model, and save it to the database."""

        obj = target_class(*args, **kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj
