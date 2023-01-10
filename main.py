import os
from datetime import datetime, timedelta, time
from collections import Counter
class PhoneCall(object):
    number   = None
    start    = None
    end      = None
    duration = None
    price    = None
    exceptions = None

    def __init__(self, data):        
        try:
            self.number = int(data[0])
            self.start = datetime.strptime(data[1], '%Y-%m-%d %H:%M:%S')
            self.end = datetime.strptime(data[2], '%Y-%m-%d %H:%M:%S')
        
            self.get_price()
        except Exception as ex:
            self.exceptions = ("Problem to parse the data. Exception: {}".format(ex))

    
    def __get_minute_rate(self, callTime) -> float:        
        if (callTime - self.start) >= timedelta(minutes=5):
            return 0.20
        elif time(hour = 8) <= callTime.time() < time(hour=16):
            return 1.00
        else:
            return 0.50

    def get_price(self) -> None:
        callTime = self.start
        totalPrice = 0.0
        for i in range(10000):
            totalPrice += self.__get_minute_rate(callTime)
            callTime += timedelta(minutes=1)
            if callTime >= self.end:
                break        
        self.price = totalPrice        


class PhoneBill(object):
        
    @staticmethod
    def get_most_used_number(phoneCalls):
        numbers       = [phoneCall.number for phoneCall in phoneCalls]
        numOccurences = Counter(numbers)    
        maxOccur      = max(numOccurences.values())
        maxKeys       = [key for key in numOccurences if numOccurences[key] == maxOccur]
        return max(maxKeys)
    
    @staticmethod
    def calculate(csvPath):
        with(open(csvPath, "r") as f):
            csvRows = f.read().split("\n")
        
        csvDatas      = [csvRow.split(",") for csvRow in csvRows if len(csvRow.split(",")) == 3]
        allPhoneCalls    = [PhoneCall(csvData) for csvData in csvDatas] 
        phoneCalls = [phoneCall for phoneCall in allPhoneCalls if phoneCall.exceptions == None]
        if len(allPhoneCalls) != len(phoneCalls):
            msg = "Some phone calls weren't properly processed:\n"
            for phoneCall in allPhoneCalls:
                if phoneCall.exceptions != None:
                    msg += phoneCall.exceptions + "\n"
            print(msg)
        mostCommonNum = PhoneBill.get_most_used_number(phoneCalls)

        price = sum([phoneCall.price for phoneCall in phoneCalls if phoneCall.number != mostCommonNum])
        print("Total price: {}".format(price))
        return price

# csvPath = r"E:\Projekty\Garrett_Test\generated_sample_2.csv"
# PhoneBill.calculate(csvPath)

    