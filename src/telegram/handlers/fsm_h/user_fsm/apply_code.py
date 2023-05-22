from aiogram import F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.database.queries import check_promo, save_code_to_user
from src.telegram.buttons import user_main_btn
from setup import user_router


class UseCode(StatesGroup):
    user_id = State()
    code = State()


@user_router.message(F.text == "Отмена")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer(
        "Отменено.",
        reply_markup=user_main_btn)


@user_router.message(UseCode.code)
async def use_code(message: Message, state: FSMContext):
    code = check_promo(message.text)
    try:
        if not code:
            raise TypeError("Не верный код!")

        save_code_to_user(message.from_user.id, code)
        await message.reply(f"Поздравляем вы успешно приминили код - `{code}`✅",
                            reply_markup=user_main_btn,
                            parse_mode="MARKDOWN")
    except Exception as err:
        await message.reply(str(err)+"❌", reply_markup=user_main_btn)
    finally:
        await state.clear()
