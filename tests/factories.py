import factory

from sqlalchemy_model_factory import SQLAlchemyModelFactory

from MonkeyBlog.models.monkey import Monkey


class MonkeyFactory(SQLAlchemyModelFactory):
    FACTORY_FOR = Monkey

    name = 'Sampo'
    email = factory.Sequence(
        lambda n: u'sampo{0}@example.com'.format(n)
    )
    age = 28
