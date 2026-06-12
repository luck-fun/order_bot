import asyncio

from aiogram import Dispatcher, Bot
from aiogram.types import BusinessConnection, Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command

from llm import llm_req

bot = Bot(token="BOT_TOKEN_HERE")
dp = Dispatcher()

photo = FSInputFile("YOUR_BIO_CARD")

class States(StatesGroup):
    get_name = State()
    get_deadline = State()
    get_price = State()
    get_techmission = State()
    get_more = State()


@dp.business_message(Command("order"))
async def state1(message: Message, state: FSMContext):
    command = message.text.split(maxsplit=1)
    global last
    last = llm_req(command[1])
    await state.set_state(States.get_name)
    await message.reply("Введите ваше имя и возраст")
    
    
@dp.business_message(States.get_name)
async def state2(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(States.get_deadline)
    await message.reply("Введите желаемые сроки выполнения")

@dp.business_message(States.get_deadline)
async def state3(message: Message, state: FSMContext):
    await state.update_data(deadline=message.text)
    await state.set_state(States.get_price)
    await message.reply("Введите ваш бюджет")
    
@dp.business_message(States.get_price)
async def state4(message: Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(States.get_techmission)
    await message.reply("Введите ТЗ или описание работы")

@dp.business_message(States.get_techmission)
async def state5(message: Message, state: FSMContext):
    await state.update_data(mission=message.text)
    await state.set_state(States.get_more)
    await message.reply(last)
    
@dp.business_message(States.get_more)
async def state6(message: Message, state: FSMContext):
    await state.update_data(more=message.text)
    data = await state.get_data()
    name = data["name"]
    deadline = data["deadline"]
    price = data["price"]
    mission = data["mission"]
    more = data["more"]
    await message.answer("Спасибо, ваш заказ в очереди. Разработчик сообщит вам в этом чате о принятии/отклонении заказа")
    await message.bot.send_message(text=f"""Заказ от @{message.from_user.username}
    Имя {name}
    Сроки {deadline}
    Бюджет {price}
    ТЗ {mission}
    Детали {more}""", chat_id="YOUR_CHAT_ID")
    await state.clear()
    

@dp.message(Command("get_id"))
async def get_id(message: Message):
    await message.bot.send_message(chat_id=message.from_user.id, text=f"@{message.from_user.username}")
    

@dp.business_message(Command("info"))
async def info(message: Message):
    conn = await message.bot.get_business_connection(
            message.business_connection_id
        )
        
    owner_id = conn.user.id

    if message.from_user.id == owner_id:
        return
    await bot.send_photo(chat_id=message.chat.id, photo=photo, business_connection_id=message.business_connection_id)
    await bot.send_message(chat_id=message.chat.id, text="""YOUR_IT_EXPIRIENCE""", business_connection_id=message.business_connection_id)

    
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())