import graphene
from graphene.relay import Node
from graphene_mongo import MongoengineConnectionField, MongoengineObjectType
from mongoengine import connect
from models import Article as ArticleModel


class Article(MongoengineObjectType):
    class Meta:
        model = ArticleModel


class Query(graphene.ObjectType):
    articles = graphene.List(Article)

    def resolve_articles(self, info):
        return list(ArticleModel.objects.all())


CONNECTION_STRING = "mongodb+srv://admin:yXNcszPcZExEiJMs@cluster0.lbaun.mongodb.net/flask_project?retryWrites=true&w=majority"
connect('flask_project', host=CONNECTION_STRING, alias='default')
schema = graphene.Schema(query=Query, types=[Article])
