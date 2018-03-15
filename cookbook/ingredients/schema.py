import graphene

from graphene_django.types import DjangoObjectType

from cookbook.ingredients.models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class IngredientType(DjangoObjectType):
    class Meta:
        model = Ingredient


class Query(object):
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    all_categories = graphene.List(CategoryType)

    ingredient = graphene.Field(IngredientType,
                                id=graphene.Int(),
                                name=graphene.String())
    all_ingredients = graphene.List(IngredientType)

    def resolve_all_categories(self, info, **kwargs):
        return Category.objects.all()

    def resolve_all_ingredients(self, info, **kwargs):
        return Ingredient.objects.all()

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    def resolve_ingredient(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Ingredient.objects.get(pk=id)

        if name is not None:
            return Ingredient.objects.get(name=name)

        return None


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(lambda: CategoryType)
    ok = graphene.Boolean()

    def mutate(self, info, name):
        category = Category.objects.create(name=name)
        ok=True
        return CreateCategory(category=category,ok=ok)


class CreateIngredient(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        notes = graphene.String(required=True)
        category = graphene.Int(required=True)

    ingredient = graphene.Field(lambda: IngredientType)
    ok = graphene.Boolean()

    def mutate(self, info, **kwargs):
        kwargs['category'] = Category.objects.get(pk=kwargs['category'])
        ingredient = Ingredient.objects.create(**kwargs)
        ok = True
        return CreateIngredient(ingredient=ingredient,ok=ok)


class Mutation(object):
    create_category = CreateCategory.Field()
    create_ingredient = CreateIngredient.Field()
