from src.database.tables import db, Account, Order, PromoCode
import string
import random

from src.schemas import AccountModel, OrderModel


def _generate_promo_code(num_char: int) -> str:
    code = ""
    symbl = string.ascii_letters + "0987654321"

    for i in range(num_char):
        code += random.choice(symbl)
    return code


def generate_new_code(num_char=10) -> str:
    code = _generate_promo_code(num_char)
    PromoCode.create(name=code)
    return code


def check_promo(name: str, incr_amount=False) -> str | None:
    promo = PromoCode.get_or_none(PromoCode.name == name)
    if not promo:
        return
    if incr_amount:
        promo.count_of_use += 1
        promo.save()
    return name


def get_all_accounts() -> list[AccountModel]:
    return [
        AccountModel(name=acc.name, price=acc.price)
        for acc in Account.select()
    ]


def get_account_by_name(name: str) -> int:
    return Account.get(name=name).id


def create_order(order=OrderModel):
    Order.create(
        user_id=order.user_id,
        account=order.account_id,
        city=order.city,
        sex=order.sex,
        with_discount=order.with_discount,
        selfie=order.selfie,
        car=order.car,
        note=order.note
    )


def get_order_by_id(order_id: int) -> OrderModel:
    order = Order.get(id=order_id)
    return OrderModel(
        user_id=order.user_id,
        account_name=order.account_name,
        city=order.city,
        sex=order.sex,
        with_discount=order.with_discount,
        disc_code=order.disc_code,
        selfie=order.selfie,
        car=order.car,
        note=order.note
    )


if __name__ == '__main__':
    acc = Account.get(name='one')
    print(acc)
