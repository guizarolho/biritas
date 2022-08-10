import requests
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


def index(request):
    return render(request, 'homepage/index.html')


@require_http_methods(['POST'])
def detail(request):
    url = "https://www.thecocktaildb.com/api/json/v1/1/search.php?"
    recipe = request.POST['recipe'].lower()
    querystring = {"s": recipe}
    response = requests.request("GET", url, params=querystring)
    data = response.json()['drinks'][0]
    return render(request, 'homepage/detail.html', {
        'drink': data['strDrink'],
        'alcoholic': data['strAlcoholic'],
        'image': data['strDrinkThumb'],
        'instructions': data['strInstructions'],
        'ingredients': zip(
            [value for key, value in data.items() if key.startswith('strIngredient') and value],
            [value for key, value in data.items() if key.startswith('strMeasure') and value],
        )
    })
