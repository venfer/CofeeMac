coffe_types = {
    1: "Эспрессо",
    2: "Американо",
    3: "Латте",
    4: "Раф",
    5: "Какао"
}
sizes = {
    1: "Маленький",
    2: "Средний",
    3: "Большой"
}
adds = {
    1: "Сахар",
    2: "Молоко",
    3: "Корица"
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



class User(object):
    """docstring"""

    def __init__(self, name):
        """Constructor"""
        self.name = name

    def Order(self):
        chosen = False;
        while chosen == False:
            print("Введите 1, чтобы выбрать Эспрессо,");
            print("Введите 2, чтобы выбрать Американо,");
            print("Введите 3, чтобы выбрать Латте,");
            print("Введите 4, чтобы выбрать Раф,");
            print("Введите 5, чтобы выбрать Какао.");
            chose = int(input("Выбор: "));
            if chose in coffe_types:
                chosen_type = coffe_types[chose];
                chosen = True;
            else:
                print("Такого варианта нет");
        chosen = False;
        while chosen == False:
            print("Введите 1, чтобы выбрать маленький,");
            print("Введите 2, чтобы выбрать средний,");
            print("Введите 3, чтобы выбрать большой.");
            chose = int(input("Выбор: "));
            if chose in sizes:
                chosen_size = sizes[chose];
                chosen = True;
            else:
                print("Такого варианта нет");
        chosen = False;
        addedsugar = 0;
        addedmilk = 0;
        addedcinnamon = 0;
        while chosen == False:
            print(f'Сейчас выбранно: {addedsugar} сахара, {addedmilk} молока, {addedcinnamon} корицы.');
            print("Введите 1, чтобы выбрать колличество сахара:");
            print("Введите 2, чтобы выбрать колличество молока:");
            print("Введите 3, чтобы выбрать колличество корицы:");
            print("Введите 4, чтобы прекратить выбор добавок.");
            chose = int(input("Выбор: "));
            if chose in adds or chose == 4:
                if chose == 1:
                    chosen_count = int(input("Колличество: "))
                    addedsugar = chosen_count;
                if chose == 2:
                    chosen_count = int(input("Колличество: "))
                    addedmilk = chosen_count;
                if chose == 3:
                    chosen_count = int(input("Колличество: "))
                    addedcinnamon = chosen_count;
                if chose == 4:
                    chosen= True;
            else:
                print("Такого варианта нет");
        ordered_cup = CofeeCup(chosen_type, chosen_size, addedsugar, addedmilk, addedcinnamon);
        return (ordered_cup)

class CofeeCup(object):

    def __init__(self, type, size, sugarcount, milkcount, cinnamoncount):
        """Constructor"""
        self.type = type
        self.size = size
        self.sugarcount = sugarcount
        self.cinnamoncount = cinnamoncount
        self.milkcount = milkcount
        self.price = types_prices[type] + sizes_prises[size] + adds_prises[1] * sugarcount + adds_prises[2] * milkcount + adds_prises[3] * cinnamoncount

if __name__ == "__main__":
    n = input("Имя? ");
    user = User(n);
    ordered_cup = user.Order();
    print(f'{ordered_cup.type} {ordered_cup.size} {ordered_cup.sugarcount} {ordered_cup.milkcount} {ordered_cup.cinnamoncount} {ordered_cup.price}')