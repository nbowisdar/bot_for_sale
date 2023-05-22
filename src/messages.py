from aiogram.types import Message

from src.database.queries import get_all_accounts
from src.schemas import OrderModel


def show_accounts_price(with_discount=False) -> str:
    msg = "\nВсе доступные аккаунты\n"
    if with_discount:
        msg = "✅Вы пременили промокод✅\n На все товары действует скидка 20%!\n" + msg
    accounts = get_all_accounts()
    for acc in accounts:
        if with_discount:
            price = f"<strike>{acc.price}</strike> => {round(acc.price/100*80)}"
        else:
            price = acc.price
        msg += f"{acc.name} - {price} руб.\n"
    return msg


def show_order(order: OrderModel, code=None) -> str:
    if order.with_discount:
        price = f"*{round(order.account_price / 100 * 80, 2)}* руб.\nСКИДКА - {round(order.account_price / 100 * 20, 2)}"
    else:
        price = order.account_price
    msg = f"""
id заказчика - [{order.user_id}](tg://user?id={order.user_id})
Username - `@{order.account_username}`
Товар - *{order.account_name}* 
Цена - {price} руб.
Город - *{order.city}*
Пол - *{order.sex}*
"""
    if order.car:
        msg += f"Машина - *{order.car}*\n"
    if order.note:
        msg += f"Коментарий - {order.note}\n"
    if code:
        msg += f'Промокод использован - `{code}`'
    return msg
