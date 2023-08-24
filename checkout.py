
'''
Confidential customer material.
-------------------------------

You are an engineer at a payment management company and you're trying to prevent users from accidentally making multiple payments to the same user.

Your task is to write a function that lets the user know if they attempt to perform another payment to the same user before a specific time limit.

You are given an integer time limit, a list of payments as a 2D array of [senderID, receiverID] pairs, and a sorted integer array of timestamps representing the time at which each payment was performed.

Your function should return a collection of strings, one for each payment, stating whether the payment could be an accidental payment to the same receiver or not. The string "true" represents an attempted new payment to the same user before the time limit, the string "false" represents a payment that has no issues.

Here are the details of the requirements:

- If the time difference between the current payment and the last payment made to the same receiver is strictly less than the time limit seconds, the function should return "true".
- The payments are given as a 2D array payments , where each element is a pair [senderID, receiverID]. 
- The corresponding timestamp for each payment is given in the timestamps array, which is sorted in ascending order.
- Use the senderID and receiverID to uniquely identify a payment.
- You need to process the payments in the order they are given in the input arrays.

Example:

timestamps_1 = [1, 4, 5, 10, 11, 14]
payments_1 = [[1, 2], [25, 65], [25, 65], [1, 2], [25,65], [1, 2]]
timelimit_1 = 5 


| Time | Sender ID | Receiver ID | Time of last payment | Result |
|------|-----------|-------------|----------------------|--------|
|    1 |         1 |           2 | --                   | False  |
|    4 |        25 |          65 | --                   | False  |
|    5 |        25 |          65 | 4                    | True   |
|   10 |         1 |           2 | 1                    | False  |
|   11 |        25 |          65 | 5                    | False  |
|   14 |         1 |           2 | 10                   | True   |


Expected answer: ["false", "false", "true", "false", "false", "true"] .


More examples:

timestamps_2 = [1, 1, 1, 11]
payments_2 =  [[1,2], [1,2], [25,35], [1,2]]
timelimit_2 = 5

In this case, there are two payments from the same sender to the same receiver at the same time, so the second payment should display "true", while the others have no issues.

timestamps_3 = [1]
payments_3 =   [[1,2]]
timelimit_3 = 5

In this example, there is only one payment, so there cannot be any issues. The expected output is a collection containing a single "false".


All test cases:
validatePayments(timestamps_1, payments_1, timelimit_1) -> ["false", "false", "true", "false", "false", "true"]
validatePayments(timestamps_2, payments_2, timelimit_2) -> ["false", "true", "false", "false"]
validatePayments(timestamps_3, payments_3, timelimit_3) -> ["false"]
validatePayments(timestamps_4, payments_4, timelimit_4) -> ["false", "false", "true", "true", "false", "false"]
validatePayments(timestamps_5, payments_5, timelimit_5) -> ["false", "true", "true", "false"]



Complexity variables:
n: the number of payments
'''

timestamps_1 = [1, 4, 5, 10, 11, 14]
payments_1 = [[1, 2], [25, 65], [25, 65], [1, 2], [25,65], [1, 2]]
timelimit_1 = 5 
#["false", "false", "true", "false", "false", "true"] 

timestamps_2 = [1, 1, 1, 11]
payments_2 =  [[1,2], [1,2], [25,35], [1,2]]
timelimit_2 = 5


timestamps_3 = [1]
payments_3 =   [[1,2]]
timelimit_3 = 5

def check_payment(timestamps, payments, limit):
    result = []
    pay_map = {}
    for i, party in enumerate(payments):
        party = str(party[0])+"_"+str(party[1])
        time = timestamps[i]
        
        if party in pay_map:
            if time - pay_map[party] < limit:
                result.append(True)
            else:
                result.append(False)
        else:
            result.append(False)
        pay_map[party] = time
    return result

# print(check_payment(timestamps_1, payments_1, timelimit_1))
# print(check_payment(timestamps_2, payments_2, timelimit_2))
# print(check_payment(timestamps_3, payments_3, timelimit_3))


'''
Confidential customer material.
-------------------------------

A quantitative trading firm processes a list of events, each of which can be classified into one of four categories:

1. BUY <stock> <quantity>: Signifies the purchase of <quantity> shares of stock <stock> at the market price.

2. SELL <stock> <quantity>: Indicates the sale of <quantity> shares of stock <stock> at the market price.

3. CHANGE <stock> <price>: Signifies a change in the market price of <stock> by <price> amount, which can be either positive or negative.

4. QUERY: Represents a query for the gross profit/loss from the start of trading to the present.

The trading firm makes a gross profit when the <stock> is bought at a lower cost and then the price increases. The trading firm suffers a loss when the <stock> is bought at a higher cost and the price decreases.

Write a function that given a list of events, returns a collection of integers representing answers to each query.


Example:

Given the list of events:

events_1 = [
    "BUY googl 20, 
    "BUY aapl 50",
    "CHANGE googl 6", 
    "QUERY",
    "SELL aapl 10",
    "CHANGE aapl -2",
    "QUERY"
    ]

The gross profit can be tracked as follows:

|     Events     |     Portfolio     | Gross Profit so far |
|----------------|-------------------|---------------------|
| BUY googl 20   | googl 20          |                   0 |
| BUY aapl 50    | googl 20, aapl 50 |                   0 |
| CHANGE googl 6 | googl 20, aapl 50 |                 120 |
| QUERY          |                   |                 120 |
| SELL aapl 10   | googl 20, aapl 40 |                 120 |
| CHANGE aapl -2 | googl 20, aapl 40 |                  40 |
| QUERY          | googl 20, aapl 40 |                  40 |


The expected result is a collection of all the query outputs: [120, 40]

----------

Other test cases:

events_2 =  ["BUY hackr 2", "QUERY"]

In this case, the expected output is [0]. The firm purchased 2 stocks of hackr, then have a "QUERY" event. Since there is no change in stock price, there is 0 gross profit so far.

events_3 = ["BUY stock2 2", "BUY stock1 4", "CHANGE stock2 -8", "SELL stock1 2", "BUY stock3 3", "QUERY"]

The price of 2 shares of stock2 decreased by 8, so the expected output is [-16].


All test cases:
getGrossProfit(events_1) -> [120, 40]
getGrossProfit(events_2) -> [0]
getGrossProfit(events_3) -> [-16]
getGrossProfit(events_4) -> [0,59296,-23980,-23980,-28780,-28780,-28780,-24126,-24126,-37939,-22188,-22188,-36894,-25824,-25824,-25824,-25824,-25824,-657052,-657052]

Complexity variables:
n: the number of events
'''

events_1 = [
    "BUY googl 20", 
    "BUY aapl 50",
    "CHANGE googl 6", 
    "QUERY",
    "SELL aapl 10",
    "CHANGE aapl -2",
    "QUERY"
    ]

events_2 =  ["BUY hackr 2", "QUERY"]

events_3 = ["BUY stock2 2", "BUY stock1 4", "CHANGE stock2 -8", "SELL stock1 2", "BUY stock3 3", "QUERY"]

def find_profit(events):
    result = []
    stock_quantity = {}
    sprice_map = {}
    profit = 0
    init_cap = {}
    cap_map = {}
    for event in events:
        vals = event.split(" ")
        if len(vals) > 1:
            sname = vals[1]
            quantity = int(vals[2])
        if vals[0] == "BUY":
            if sname in stock_quantity:
                stock_quantity[sname]+= quantity
                cap_map+=quantity*sprice_map[sname]
            else:
                stock_quantity[sname] = quantity
                sprice_map[sname] = 1
                init_cap[sname] = quantity
                cap_map[sname]=0
        if vals[0] == "SELL":
            stock_quantity[sname] -= quantity
            # sprice_map[sname] = 0
            cap_map[sname]+=quantity*sprice_map[sname]
            # profit+=quantity*sprice_map[sname]
        if vals[0] == "CHANGE":
            # sprice_map[sname]+=quantity
            cap_map[sname]+=stock_quantity[sname]*(int(vals[2]))
            print(profit, stock_quantity[sname],(int(vals[2])))
            profit+=stock_quantity[sname]*(int(vals[2]))
            
        if vals[0] == "QUERY":
            result.append(profit)

    if len(result) == 0:
        result.append(0)
    # else:
    return result

print(find_profit(events_1))
print(find_profit(events_2))
print(find_profit(events_3))
