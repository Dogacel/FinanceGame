import urllib.parse, urllib.request
import pickle
from yahoo_finance import Share

def get_data(finance_code):
    str = "https://www.google.com/finance/historical?q=" + urllib.parse.quote_plus(finance_code) + "&output=csv"
    try:
        with urllib.request.urlopen(str) as f:
            with open('./data./'+urllib.parse.quote_plus(finance_code)+'.csv', 'wb+') as file:
                file.write(f.read())
    except Exception as e:
        print(e)

def load(id):
    tmp = player()
    try:
        return pickle.load(open("./data/" + str(id) +".data", "rb"))
    except (Exception) as e:
        print(e)
    return tmp

def fin_exist(finance_code):
    t = Share(finance_code)
    if t.get_name() != None:
        return True
    return False

def _fin_exist(finance_code):
    str = "https://www.google.com/finance?q=" + urllib.parse.quote_plus(finance_code)
    try:
        with urllib.request.urlopen(str) as f:
            return True
    except Exception as e:
        print("No data found")
        return False

class player:

    def __init__(self, finance_data={'USD': 1000}, personal_data={},):
        self.finance_data = finance_data
        self.personal_data = personal_data
    
    def setID(self, id):
        self.personal_data["id"] = str(id)

    def about(self):
        print(self.personal_data)
    
    def showmethebank(self):
        print(self.finance_data)

    def save(self):
        if "id" in self.personal_data:
            with open("./data/"+ str(self.personal_data["id"] + ".data"), 'wb+') as f:
                pickle.dump(self, f)

    def feed(self, code, amount):
        if not fin_exist(code):
            return False
        if self.finance_data['USD'] >= amount:
            share = Share(code)
            share.refresh()
            self.finance_data['USD'] -= amount
            if code not in self.finance_data:
                self.finance_data[code] = amount/float(share.get_price())
            else:
                self.finance_data[code] += amount/float(share.get_price())
            return True
        return False
    
    def net_worth(self):
        net = 0
        for key in self.finance_data:
            if key == "USD":
                net += self.finance_data[key]
            else:
                if self.finance_data[key] != 0:
                    share = Share(key)
                    share.refresh()
                    net += self.finance_data[key]*float(share.get_price())
        return net

    def pull(self, code, amount):
        if code in self.finance_data:
            share = Share(code)
            share.refresh()
            self.finance_data[code] -= amount
            self.finance_data['USD'] += amount*float(share.get_price())
            return True
        return False


p = player()
p = load(270199)

print(p.net_worth())

p.showmethebank()