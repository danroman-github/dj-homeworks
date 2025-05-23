from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }

def recipe_views(request, dish_name):
    recipe = DATA.get(dish_name)

    if recipe is None:
        context = {'recipe': None}
    else:
        servings = request.GET.get('servings')

        if servings and servings.isdigit() and int(servings) > 0:
            servings = int(servings)
            adjusted_recipe = {}
            for ingredient, amount in recipe.items():
                adjusted_recipe[ingredient] = amount * servings
            context = {'recipe': adjusted_recipe}
        else:
            context = {'recipe': recipe}

    return render(request, 'calculator/index.html', context)