#  Created by btrif Trif on 21-02-2023 , 6:15 PM.

#   Taken from :  https://github.com/eugeneyan/fastapi-html


from fastapi import APIRouter, Request, Form

from fastapi.templating import Jinja2Templates
from starlette.responses import FileResponse

html_router = APIRouter(
        prefix="",
        tags=["HTML"],
        # dependencies=[Depends(TokenSchema)],
        responses={404: {"description": "Not found"}},
        )


def spell_number(num: int, multiply_by_2: bool = False):
    d = {
        0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
        6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
        11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
        15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
        19: 'nineteen', 20: 'twenty',
        30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty',
        70: 'seventy', 80: 'eighty', 90: 'ninety'
        }
    k = 1000
    m = k * 1000
    b = m * 1000
    t = b * 1000

    assert (0 <= num)

    if multiply_by_2:
        num *= 2

    if num < 20:
        return d[num]

    if num < 100:
        if num % 10 == 0:
            return d[num]
        else:
            return d[num // 10 * 10] + '-' + d[num % 10]

    if num < k:
        if num % 100 == 0:
            return d[num // 100] + ' hundred'
        else:
            return d[num // 100] + ' hundred and ' + spell_number(num % 100)

    if num < m:
        if num % k == 0:
            return spell_number(num // k) + ' thousand'
        else:
            return spell_number(num // k) + ' thousand, ' + spell_number(num % k)

    if num < b:
        if (num % m) == 0:
            return spell_number(num // m) + ' million'
        else:
            return spell_number(num // m) + ' million, ' + spell_number(num % m)

    if num < t:
        if (num % b) == 0:
            return spell_number(num // b) + ' billion'
        else:
            return spell_number(num // b) + ' billion, ' + spell_number(num % b)

    if num % t == 0:
        return spell_number(num // t) + ' trillion'
    else:
        return spell_number(num // t) + ' trillion, ' + spell_number(num % t)


def save_to_text(content, filename):
    filepath = 'static/{}.txt'.format(filename)
    with open(filepath, 'w') as f:
        f.write(content)
    return filepath


#########   HTML ROUTES     ########


templates = Jinja2Templates(directory='static/')


@html_router.get('/form')
def form_post(request: Request):
    result = 'Type a number'
    # templates.TemplateResponse(' ')
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result})


@html_router.post('/form')
def form_post(request: Request, num: int = Form(...)):
    result = spell_number(num)
    return templates.TemplateResponse('form.html', context={'request': request, 'result': result, 'num': num})


@html_router.get('/checkbox')
def form_post(request: Request):
    result = 'Type a number'
    return templates.TemplateResponse('checkbox.html', context={'request': request, 'result': result})


@html_router.post('/checkbox')
def form_post(request: Request, num: int = Form(...), multiply_by_2: bool = Form(False)):
    result = spell_number(num, multiply_by_2)
    return templates.TemplateResponse('checkbox.html', context={'request': request, 'result': result, 'num': num})


@html_router.get('/download')
def form_post(request: Request):
    result = 'Type a number'
    return templates.TemplateResponse('download.html', context={'request': request, 'result': result})


@html_router.post('/download')
def form_post(request: Request, num: int = Form(...), multiply_by_2: bool = Form(False), action: str = Form(...)):
    if action == 'convert':
        result = spell_number(num, multiply_by_2)
        return templates.TemplateResponse(
                'download.html', context={'request': request, 'result': result, 'num': num}
                )
    elif action == 'download':
        # Requires aiofiles
        result = spell_number(num, multiply_by_2)
        filepath = save_to_text(result, num)
        return FileResponse(filepath, media_type='application/octet-stream', filename='{}.txt'.format(num))
