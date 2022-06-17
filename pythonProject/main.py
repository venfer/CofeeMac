import pg8000

from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, ForeignKey, Boolean

meta = MetaData()

users = Table('Users', meta,
    Column('User_ID', Integer, primary_key = True),
    Column('User_name', String(250), nullable = False),
    Column('Admin_roots', Boolean, nullable = False)
)

coffes = Table('Coffe_orders', meta,
    Column('Order_ID', Integer, primary_key = True),
    Column('Orderer_name', String(250), nullable = False),
    Column('Coffe_type', String(250), nullable = False),
    Column('Coffe_size', String(250), nullable = False),
    Column('Sugar_count', Integer, nullable = False),
    Column('Milk_count', Integer, nullable = False),
    Column('Cinnamon_count', Integer, nullable = False),
    Column('Price', Integer, nullable = False)
)

engine = create_engine("postgresql+pg8000://postgres:root@localhost/BedaSDB", echo = True)
meta.create_all(engine)

con = engine.connect()

coffe_types = {
    '1': "Эспрессо",
    '2': "Американо",
    '3': "Латте",
    '4': "Раф",
    '5': "Какао"
}
sizes = {
    '1': "Маленький",
    '2': "Средний",
    '3': "Большой"
}
types_prices = {
    "Эспрессо": 153,
    "Американо": 112,
    "Латте": 11,
    "Раф": 122,
    "Какао": 432
}
sizes_prises = {
    "Маленький": 32,
    "Средний": 44,
    "Большой": 55
}
adds_prises = {
    1: 12,
    2: 3,
    3: 21
}

class CofeeMachine(object):

    def SetScreen(self, screen):
        self.screen = screen

    def ChooseUser(self):
        self.screen.StartInput()
        intruder = input();
        result1 = users.select().where(users.c.User_name == intruder)
        result2 = con.execute(result1)
        result3 = result2.fetchall()
        if len(result3) != 0:
            current_user = User(result3[0][1], result3[0][2])
        else:
            self.screen.ChooseCreate()
            while True:
                chose = input();
                if chose == '1' or chose == '2':
                    if chose == '1':
                        current_user = self.CreateUser(intruder);
                        break
                    if chose == '2':
                        self.ChooseUser()
                else: self.screen.ErorrMessage()
        self.MainMenu(current_user)

    def Cook_Coffee(self):
        coffee_cup = CofeeCup();
        while True:
            self.screen.TypeInfo();
            if coffee_cup.Set_Type(): break
            self.screen.ErorrMessage()
        while True:
            self.screen.SizeInfo();
            if coffee_cup.Set_Size(): break
            self.screen.ErorrMessage()
        while True:
            self.screen.SugarInfo();
            if coffee_cup.Set_Sugar(): break
            self.screen.ErorrMessage()
        while True:
            self.screen.MilkInfo();
            if coffee_cup.Set_Milk(): break
            self.screen.ErorrMessage()
        while True:
            self.screen.CinnamonInfo();
            if coffee_cup.Set_Cinnamon(): break
            self.screen.ErorrMessage()
        return (coffee_cup)

    def Give_Price(self, coffee_cup):
        return (coffee_cup.price)

    def CreateUser(self, name):
        self.screen.AdminInfo()
        while True:
            chose = input();
            if chose == '1' or chose == '2':
                if chose == '1':
                    is_admin = True;
                    break
                if chose == '2':
                    is_admin = False
                    break
            else:
                self.screen.ErorrMessage()
        user_ad = users.insert().values(User_name = name, Admin_roots = is_admin)
        con.execute(user_ad)
        return (User(name, is_admin))

    def MainMenu(self, current_user):
        if current_user.is_admin == True:
            self.screen.AdminMenu()
            while True:
                chose = input()
                if chose == '1' or chose == '2' or chose == '3' or chose == '4':
                    if chose == '1':
                         self.Cook_Coffee()
                         break
                    if chose == '2':
                         self.GiveCofeeCup()
                    if chose == '3':
                         self.Cook_Coffee()
                         break
                    if chose == '4':
                        self.ChooseUser()
                else: self.screen.ErorrMessage()
        else:
            self.screen.UserMenu()
            while True:
                chose = input()
                if chose == '1' or chose == '2':
                    if chose == '1':
                         self.GiveCofeeCup(current_user)
                         break
                    if chose == '2':
                        self.ChooseUser()
                        break
                else: self.screen.ErorrMessage()
        self.MainMenu(current_user)

    def GiveCofeeCup(self, current_user):
        order = self.Cook_Coffee()
        cup_add = coffes.insert().values(Orderer_name = current_user.name, Coffe_type = order.type, Coffe_size = order.size, Sugar_count = order.sugar, Milk_count = order.milk, Cinnamon_count = order.cinnamon, Price = order.Count_Price())
        con.execute(cup_add)
        return order

class Screen(object):

    def __init__(self, cofee_machin):
        """Constructor"""
        self.coffe_machin = cofee_machin
        self.coffe_machin.SetScreen(self);
        self.current_user = self.coffe_machin.ChooseUser()
        self.current_user = self.coffe_machin.CreateUser(self.current_user)

    def StartInput(self):
        print("Введите имя пользователя: ")

    def CoffeeGiven(self):
        print("Вот ваш кофе. ")

    def AdminMenu(self):
        print("Введите 1, чтобы получить список всех пользователей,");
        print("Введите 2, чтобы заказать кофе,");
        print("Введите 3, чтобы получить список всех заказов,");
        print("Введите 4, чтобы выйти.");

    def UserMenu(self):
        print("Введите 1, чтобы заказать кофе,");
        print("Введите 2, чтобы выйти.");

    def AdminInfo(self):
        print("Введите 1, если данный пользователь является администратором,");
        print("Введите 2, если данный пользователь не является администратором.");

    def ChooseCreate(self):
        print("Такого пользователя нет, создать пользователя с таким именем? Введите 1, если да или 2, если нет.")

    def MainMenu(self, currentUser):
        print("Введите 1, чтобы заказать кофе,");
        print("Введите 2, чтобы сменить пользователя,");

    def TypeInfo(self):
            print("Введите 1, чтобы выбрать Эспрессо,");
            print("Введите 2, чтобы выбрать Американо,");
            print("Введите 3, чтобы выбрать Латте,");
            print("Введите 4, чтобы выбрать Раф,");
            print("Введите 5, чтобы выбрать Какао.");

    def SizeInfo(self):
            print("Введите 1, чтобы выбрать маленький,");
            print("Введите 2, чтобы выбрать средний,");
            print("Введите 3, чтобы выбрать большой.");

    def SugarInfo(self):
        print("Введите желаемое колличество сахара.");

    def MilkInfo(self):
        print("Введите желаемое колличество молока.");

    def CinnamonInfo(self):
        print("Введите желаемое колличество корицы.");

    def ErorrMessage(self):
        print('Такого выбора нет!')

class User(object):
    """docstring"""
    def __init__(self, name, is_admin):
        """Constructor"""
        self.name = name
        self.is_admin = is_admin

class CofeeCup(object):

    def Set_Type(self):
        chosen = input()
        if chosen in coffe_types:
            self.type = coffe_types[chosen];
            return True
        else:
            return False

    def Set_Size(self):
        chosen = input()
        if chosen in sizes:
            self.size = sizes[chosen];
            return True
        else:
            return False

    def Set_Sugar(self):
        chosen = int(input())
        if chosen > -1:
            self.sugar = chosen
            return True
        else:
            return False

    def Set_Milk(self):
        chosen = int(input())
        if chosen > -1:
            self.milk = chosen
            return True
        else:
            return False

    def Set_Cinnamon(self):
        chosen = int(input())
        if chosen > -1:
            self.cinnamon = chosen
            return True
        else:
            return False

    def Count_Price(self):
        return types_prices[self.type] + sizes_prises[self.size] + adds_prises[1] * self.sugar + adds_prises[2] * self.milk + adds_prises[3] * self.cinnamon


if __name__ == "__main__":
    my_machine = CofeeMachine()
    my_screen = Screen(my_machine)