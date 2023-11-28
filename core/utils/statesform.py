from aiogram.fsm.state import StatesGroup, State


# class StepsForm(StatesGroup):
#     GET_FUNCTION = State()
#     ADD_STAR = State()
#     ADD_IMAGE = State()

class StepsForm(StatesGroup):
    GET_FORWARDS_MESSAGE = State()


class SenderSteps(StatesGroup):
    GET_MESSAGE = State()
    Q_BUTTON = State()
    GET_BUTTON = State()
    GET_URL_BUTTON = State()
    Q_IMAGE = State()
    GET_IMAGE = State()
