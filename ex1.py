import random
import json
import sys
import pandas

# global fixed variables
reorderLevel = 30
reorderUptoLevel = 60

# step: randomdigits
randomdigits = json.dumps({
    "0": "19223",
    "1": "16034",
    "2": "05756",
    "3": "28713",
    "4": "96409",
    "5": "12531",
    "6": "42544",
    "7": "82853",
    "8": "73676",
    "9": "47150",
    "10": "99400",
    "11": "01927",
    "12": "27754",
    "13": "42648",
    "14": "82425",
    "15": "36290",
    "16": "45467",
    "17": "71709",
    "18": "77558",
    "19": "00095",
    "20": "32863",
    "21": "29485",
    "22": "82226",
    "23": "90056",
    "24": "52711"})

# find value from dictionary
def DailyDemand(step):
    valuedigits = 0
    digits = json.loads(randomdigits)
    for time, fivedigits in digits.items():
        if time == str(step):
            valuedigits = fivedigits
    return valuedigits

# quantity depends on given table/dictionary
def DecisionofQuantity(valuedigits):
    demandquantity = int(valuedigits[:4])
    if demandquantity >= 0 and demandquantity <= 1666:
        qtt = 5
    elif demandquantity > 1666 and demandquantity <= 3333:
        qtt = 6
    elif demandquantity > 3333 and demandquantity <= 5000:
        qtt = 7
    elif demandquantity > 5000 and demandquantity <= 6666:
        qtt = 8
    elif demandquantity > 6666 and demandquantity <= 8333:
        qtt = 9
    elif demandquantity > 8333 and demandquantity <= 9999:
        qtt = 10
    else:
        print("Something wrong. ")
        qtt = 0
    return qtt

# how many stock do we need(30 <= stock =< 60)
def QttofDelivery():
    deliveryquantity = reorderUptoLevel - quantityInStock
    return deliveryquantity

# time need to be delivered. (consumes steps)
def DeliveryTime(valuedigits):
    timeschedule = int(valuedigits[4:])
    if timeschedule == 1 or timeschedule == 2:
        execution = 1
    elif timeschedule >= 3 and timeschedule < 8:
        execution = 2
    elif timeschedule == 8 or timeschedule == 9 or timeschedule == 0:
        execution = 3
    else:
        print("Something goes wrong. ")
        sys.exit()
    return execution

# reorder
def quantityCheck(valuedigits):
    delivered = QttofDelivery()
    schedule = step + DeliveryTime(valuedigits)
    # print("Del{"+str(delivered)+"}@" + str(schedule))
    delevent = ", Del{" + str(delivered) + "}@" + str(schedule)
    return schedule, delivered, delevent

def DeliveryProcess(id, timing, delivered):
    if int(id) == int(timing):
        stockNow = quantityInStock + delivered
    else:
        stockNow = quantityInStock
    return stockNow

# when scheduled step comes, delivery must be executed.
def DeliveryCheck(schedule, id, delivered):
    stck = DeliveryProcess(id, schedule, delivered)
    return stck



if __name__ == '__main__':
    print("Inventory Management Model".center(60, "-"))
    header = ['Step', 'quantityInStock', 'UpcomingEvents']
    print('%12s  %12s  %12s' % (header[0], header[1], header[2]))
    ############################## initialization ##############################
    step = 0
    quantityInStock = 50
    quantity = 0
    upcoming = 0
    expectation = 0
    events = []
    phase = []
    qIS = []
    # If DailyDemand and Delivery happen simultaneously,
    # Delivery must be executed at first.

    for i in range(25): # 25 steps
        phase.append(step)
        qIS.append(quantityInStock)
        # print("step: " + str(step) + "\nquantity in stock : " + str(quantityInStock))
        five = DailyDemand(step)
        demand = DecisionofQuantity(five)

        if quantityInStock > reorderLevel:
            events.append("")
            pass
        elif quantityInStock < 30:
            if upcoming == 0:
                upcoming, expectation, delplan = quantityCheck(five)
                events.append(delplan)
            elif upcoming != 0 and upcoming > step:
                events.append("")
                pass
            elif upcoming == step:
                dlvdstk = DeliveryCheck(upcoming, step, expectation)
                quantityInStock = dlvdstk
                upcoming = 0
                events.append("")
        else:
            pass
        show = "Demand{" + str(demand) + "}@" + str(step) + events[i]
        print('%12s | %12s | %12s' % (str(phase[i]), str(qIS[i]), show))
        quantityInStock = quantityInStock - demand
        step += 1

        if quantityInStock < 0:
            print("This is big problem. ")
            sys.exit()
        else:
            pass
