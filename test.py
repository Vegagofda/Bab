import pyupbit
import time
import requests

# Token, channel, 접속api
myToken = "xoxb-3121263311895-3132979792373-nEzwuoKivNKJgalSOk3UpqhG"
profit = "#수익"
purchase = "#매수"

def post_message(token, channel, text):
    response = requests.post("https://slack.com/api/chat.postMessage",
                             headers={"Authorization": "Bearer " + token},
                             data={"channel": channel, "text": text}
                             )
    print(response)

access = "thmnBbvEVfEXvULIR6APykehoIRLVq3xT0LfbtfR"
secret = "X5MjoMGLycChAxMrItTgac4y91awKvTwFIAiJYpT"
upbit = pyupbit.Upbit(access, secret)

# 거래 비율
plus_rate = 2.5/100  # 최종 익절 비율(%)
midsell_rate = 5/100 # 중간매도 익절 비율(%)
minus_rate = 5/100  # 최소 낙차 비율(%)
high_rate = 5/100 # 고점 생성 비율(%)
base_price = 5000
n = 20
base_a = 0.7
if 'sum_get' in globals():
    pass
else:
    global sum_get
    sum_get = 0

# 코인 선택
# 거래 종목 지정 지정. 안할 시 전체 코인 거래
PASS = ['KRW-BTT']# ['KRW-ARK', 'KRW-XRP', 'KRW-STRK', 'KRW-MED', 'KRW-BTC', 'KRW-MANA', 'KRW-SAND', 'KRW-ETH']
# SELECTED_COINS = ['KRW-BTC','KRW-ETH']# ['KRW-ARK', 'KRW-XRP', 'KRW-STRK', 'KRW-MED', 'KRW-BTC', 'KRW-MANA', 'KRW-SAND', 'KRW-ETH']
SELECTED_COINS = pyupbit.get_tickers(fiat = 'KRW')
# print(SELECTED_COINS)
# print(len(SELECTED_COINS))
# 종목별 상수 a, set_Base_price
set_a = [{'market':'KRW-BTC', 'a':0.6, 'set_base_price':10000}, {'market':'KRW-ETH', 'a':0.6, 'set_base_price':10000}]
list_a=[]
for i in range(len(set_a)):
    list_a.append(set_a[i]['market'])
# 업비트 거래 목록
coins = pyupbit.get_tickers(fiat = 'KRW')
tickers = pyupbit.get_tickers(fiat='KRW', verbose=True, is_details=True)#{[krw-ark,아크,유의종목,],....}

k = len(tickers)
for j in range(k):
    market_warning = (tickers[j]['market_warning'])
    market = (tickers[j]['market'])
    kor = (tickers[j]['korean_name'])
    set_market = [market]
    locals()[market+'L{}'.format(0)] = 1

    if set(set_market) & set(PASS):
        pass
    elif set(list_a)&set(set_market):        
        a=set_a[list_a.index(market)]['a']
        k = 0
        for i in range(1, n + 1):
            locals()[market+'K{}'.format(i)] = round(2 ** (a ** (1 / 2) * (i-1) / 4), 2)
            k += locals()[market+'K{}'.format(i)]
            L = 0
            for j in range(1,i+1):
                L += (locals()[market+'K{}'.format(j)])*(1-minus_rate)**(i-j)
            locals()[market+'KN{}'.format(i)] = k
            locals()[market+'L{}'.format(i)] = L/locals()[market+'KN{}'.format(i)]
    else:
        a=base_a
        k = 0
        for i in range(1, n + 1):
            locals()['K{}'.format(i)] = round(2 ** (a ** (1 / 2) * (i-1) / 4), 2)
            k += locals()['K{}'.format(i)]
            L = 0
            for j in range(1,i+1):
                L += (locals()['K{}'.format(j)])*(1-minus_rate)**(i-j)
            locals()['KN{}'.format(i)] = k
            locals()['L{}'.format(i)] = L/locals()['KN{}'.format(i)]
locals()[market+'L{}'.format(0)] = 1+minus_rate
locals()['L{}'.format(0)] = 1+minus_rate
locals()[market+'KN{}'.format(0)]=0
locals()['KN{}'.format(0)]=0
# print(locals()['L{}'.format(0)])
# for i in range(1, n + 1):
#     print(locals()['K{}'.format(i)])
# for i in range(1, n + 1):
#     print(locals()['KN{}'.format(i)])
# for i in range(1, n+1):
#     print(locals()['L{}'.format(i)])
if __name__ == '__main__':
    while True:
        k = len(tickers)
        for j in range(k):
            market_warning = (tickers[j]['market_warning'])
            market = (tickers[j]['market'])
            kor = (tickers[j]['korean_name'])
            set_market = [market]
            price = pyupbit.get_current_price(market)  # 현재 가격
            coin_number = upbit.get_balance(market)  # 현재 코인수
            # Price_mid = upbit.get_avg_buy_price(market)  # 현재 평단가
            price_now = price * coin_number  # 현재 평가금액
            # price_sum = Price_mid * coin_number  # 현재 투자금액
            price_sum = upbit.get_amount(market) # 투자금액(원금)
            bank = upbit.get_balance("KRW")  # 현재 잔고금액
            high_price=0
            if set(set_market) & set(PASS):
                continue
            elif set(list_a)&set(set_market):
                for r in range(len(list_a)):
                    if market == set_a[r]['market']:
                        set_base_price = set_a[r]['set_base_price']
                        for i in range(1, n+1):
                            if price_sum > locals()[market+'KN{}'.format(i)] * set_base_price * 0.99:
                                pass
                            else:
                                trade_num = i
                                break
                        trade_price = locals()[market+'K{}'.format(trade_num)] * set_base_price
                        line = locals()[market+'L{}'.format(trade_num-1)]
                        if trade_num > 1:
                            midsell_price = locals()[market+'K{}'.format(trade_num-1)] * set_base_price
                        break
            else:
                set_base_price = base_price
                for i in range(1, n+1):
                    if price_sum > locals()['KN{}'.format(i)] * set_base_price * 0.99:
                        pass
                    else:
                        trade_num = i
                        break
                trade_price = locals()['K{}'.format(trade_num)] * set_base_price
                line = locals()['L{}'.format(trade_num-1)]
                if trade_num > 1:
                   midsell_price = locals()['K{}'.format(trade_num-1)] * set_base_price

                ################### 매수 ####################
            if trade_price < bank:
                if price_now <= price_sum * (line-minus_rate):
                    print(market)
                    print(trade_num, "차매수", "(",100-(trade_num * minus_rate - minus_rate)*100, "%)")
                    bank_in = upbit.get_balance("KRW")
                    print(upbit.buy_market_order(market,trade_price))
                    time.sleep(2)
                    bank_out = upbit.get_balance("KRW")
                    print("%s"' '"%d""%s" % ("체결가", price, "원"))
                    print("%s"' '"%d""%s" % ("투입금", bank_in - bank_out, "원"))
                    Price_mid = upbit.get_avg_buy_price(market)
                    coin_number = upbit.get_balance(market)
                    print("%s"' '"%d""%s" % ("누적투입금", price_sum, "원"))
                    print("%s"' '"%d""%s" % ("현금잔고", bank_out, "원"))

                    post_message(myToken, purchase, str(trade_num) + "차매수" + str(market) + ""
                                                                                            "` (체결가" + str(
                        int(price)) + "원)"
                                        "\n 투입금" + str(int(bank_in - bank_out)) + "원"
                                                                                "\n 누적투입금" + str(
                        int(trade_price * locals()['KN{}'.format(trade_num)])) + "원"
                                                                    "\n 현금잔고" + str(int(bank_out)) + "원")
                    continue
                ################### 매도 ####################

            if price_now >= 5000:
                # if Changed_Mid_Price * (1 + High_rate / 100) <= price or Price_now > globals()['PN{}'.format(trade_num)] * (1 + High_rate / 100):
                if price_now > price_sum * (1 + high_rate):
                    if market+'{}'.format('high_price') in globals():
                        high_price = globals()[market+'{}'.format('high_price')]
                    else:
                        high_price = 0
                        globals()[market+'{}'.format('high_price')] = 0
                    if price > high_price:
                        globals()[market+'{}'.format('high_price')] = price
                        print(str(market) + " 익절 고점 생성 " + str(price))
                        continue
                # if 0 < price <= high_price * (1 - Plus_rate / 100) and Price_now > globals()['PN{}'.format(trade_num)] * (1 + Plus_rate / 100):
                    elif price <= high_price * (1 - plus_rate) and price_now > price_sum * (
                            1 + plus_rate):
                        print(market)
                        print("익절")
                        print(upbit.sell_market_order(market, coin_number))
                        time.sleep(2)
                        bank_out = upbit.get_balance("KRW")
                        print("%s"' '"%d""%s" % ("체결가", price, "원"))
                        print("%s"' '"%d""%s" % ("수익금", bank_out - bank - price_sum, "원"))
                        print("%s"' '"%s""%s" % (
                            "수익률", str(round((bank_out - bank - price_sum) / price_sum * 100, 2)), "%"))
                        print("%s"' '"%d""%s" % ("현금잔고", bank_out, "원"))
                        sum_get = sum_get + bank_out - bank - price_sum * 1.0005

                        post_message(myToken, profit, profit + str(market) + ""
                                                                            "` (체결가" + str(int(price)) + "원)"
                                                                                                        "\n 수익금" + str(
                            int(bank_out - bank - price_sum * 1.0005)) + "원"
                                                                        "\n 수익률" + str(
                            round((bank_out - bank - price_sum * 1.0005) / price_sum * 100, 2)) + "%"
                                                                                                "\n일일누적" + str(
                            int(sum_get)) + "원"
                                            "\n현금잔고" + str(int(bank_out)) + "원")
                        del locals()[market+'{}'.format('high_price')]
                        continue
                    else:
                        continue

                ################## 중간매도 ####################
                if price_now >= price_sum * (line + midsell_rate) and trade_num > 1:
                    if market+'{}'.format('high_price') in globals():
                        high_price = globals()[market+'{}'.format('high_price')]
                    else:
                        high_price = 0
                        globals()[market+'{}'.format('high_price')] = 0
                    if price > high_price:
                        globals()[market+'{}'.format('high_price')] = price
                        print(str(market) + " 중간매도 고점 생성 " + str(price))
                        continue
            
                    elif price <= high_price * (1 - plus_rate) and price_now >= price_sum * (line + plus_rate):
                        sell_coins = midsell_price / price
                        bank_in = upbit.get_balance("KRW")
                        print(market)
                        print(trade_num, "차매도")
                        print(upbit.sell_market_order(market, sell_coins))
                        time.sleep(2)
                        bank_out = upbit.get_balance("KRW")
                        Price_mid = upbit.get_avg_buy_price(market)
                        coin_number = upbit.get_balance(market)
                        print("%s"' '"%d""%s" % ("현금잔고", bank_out, "원"))
                        post_message(myToken, purchase, str(trade_num) + "차매도" + str(market) + "(체결가" + str(
                            price) + "원)" + "\n 매도금" + str(int(bank_out - bank_in)) + "원" + "\n 누적투입금" + str(
                            (price_sum)) + "원" + "\n 현금잔고" + str(int(bank_out)) + "원")
                        del locals()[market+'{}'.format('high_price')]
                        continue
                if high_price > 0 and price_now < price_sum * line * (1 + plus_rate) and price_now < price_sum * (1 + plus_rate):
                    del globals()[market+'{}'.format('high_price')]
                    print('고점 삭제')
            time.sleep(1)  # if_elif 내부코딩간의진행간격(초)