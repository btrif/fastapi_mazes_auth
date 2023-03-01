#  Created by btrif Trif on 21-02-2023 , 6:15 PM.

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from fastapi import Depends, FastAPI, HTTPException, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from src.mazes.utils import get_current_user
from src.mazes.crud import create_user_item, get_items
from src.mazes.database import get_db
from src.mazes.schemas import UserSchema, ItemCreateSchema, ItemSchema


html_router = APIRouter(
        prefix="",
        tags=["HTML"],
        # dependencies=[Depends(TokenSchema)],
        responses={404: {"description": "Not found"}},
        )




def spell_number(num: int, multiply_by_2: bool = False):
    d = {0: 'zero', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five',
         6: 'six', 7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten',
         11: 'eleven', 12: 'twelve', 13: 'thirteen', 14: 'fourteen',
         15: 'fifteen', 16: 'sixteen', 17: 'seventeen', 18: 'eighteen',
         19: 'nineteen', 20: 'twenty',
         30: 'thirty', 40: 'forty', 50: 'fifty', 60: 'sixty',
         70: 'seventy', 80: 'eighty', 90: 'ninety'}
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


'''

@items_router.post("/create_item", response_model=ItemSchema)
def create_item_for_user_only_if_authenticated(
        item: ItemCreateSchema,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(get_current_user)
        ) :
    user_id = current_user.id

    return create_user_item(db=db, item=item, user_id=user_id)



@items_router.get("/items", response_model=list[ ItemSchema ])
def list_all_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)) :
    items = get_items(db, skip=skip, limit=limit)
    return items

'''