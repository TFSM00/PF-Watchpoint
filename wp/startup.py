from wp.pages import menu
from wp.utils import Utils


def startup():
    menu()
    Utils.init_db()