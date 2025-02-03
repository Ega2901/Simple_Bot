import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import PollAnswer
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import os

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

class Survey(StatesGroup):
    question_1 = State()
    question_2 = State()
    question_3 = State()

questions = [
    "Оцените качество обслуживания",
    "Насколько быстро решена ваша проблема",
    "Насколько вежлив был сотрудник"
]

user_responses = {}

@dp.message(lambda message: message.text == '/start')
async def start_survey(message: types.Message, state: FSMContext):
    user_responses[message.from_user.id] = []
    await bot.send_poll(
        chat_id=message.chat.id,
        question=questions[0],
        options=["1", "2", "3", "4", "5"],
        is_anonymous=False
    )
    await state.set_state(Survey.question_1)

@dp.poll_answer()
async def handle_poll_answer(poll_answer: PollAnswer, state: FSMContext):
    user_id = poll_answer.user.id
    answer = poll_answer.option_ids[0] + 1
    user_responses[user_id].append(answer)

    current_state = await state.get_state()
    if current_state == Survey.question_1.state:
        await bot.send_poll(
            chat_id=poll_answer.user.id,
            question=questions[1],
            options=["1", "2", "3", "4", "5"],
            is_anonymous=False
        )
        await state.set_state(Survey.question_2)
    elif current_state == Survey.question_2.state:
        await bot.send_poll(
            chat_id=poll_answer.user.id,
            question=questions[2],
            options=["1", "2", "3", "4", "5"],
            is_anonymous=False
        )
        await state.set_state(Survey.question_3)
    elif current_state == Survey.question_3.state:
        avg_score = sum(user_responses[user_id]) / len(user_responses[user_id])
        await bot.send_message(poll_answer.user.id, f"Спасибо за участие! Ваша средняя оценка: {avg_score:.2f}")
        await state.clear()

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
