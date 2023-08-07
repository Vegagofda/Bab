import pyupbit
import time

access = "thmnBbvEVfEXvULIR6APykehoIRLVq3xT0LfbtfR"
secret = "X5MjoMGLycChAxMrItTgac4y91awKvTwFIAiJYpT"
upbit = pyupbit.Upbit(access, secret)

# 거래 비율
plus_rate = 2.5/100  # 최종 익절 비율(%)
minus_rate = 5/100  # 최소 낙차 비율(%)
high_rate = 5/100 # 고점 생성 비율(%)
midsell_rate = minus_rate + high_rate # 중간매도 익절 비율(%)
base_price = 5000
n = 20
base_a = 0.7
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
                    print(upbit.buy_market_order(market,trade_price))
                    time.sleep(2)
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
                        continue
                # if 0 < price <= high_price * (1 - Plus_rate / 100) and Price_now > globals()['PN{}'.format(trade_num)] * (1 + Plus_rate / 100):
                    elif price <= high_price * (1 - plus_rate) and price_now > price_sum * (1 + plus_rate):
                        print(upbit.sell_market_order(market, coin_number))
                        time.sleep(2)
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
                        continue
            
                    elif price <= high_price * (1 - plus_rate) and price_now >= price_sum * (line + plus_rate):
                        sell_coins = midsell_price / price
                        print(upbit.sell_market_order(market, sell_coins))
                        time.sleep(2)
                        del locals()[market+'{}'.format('high_price')]
                        continue
                if high_price > 0 and price_now < price_sum * line * (1 + plus_rate) and price_now < price_sum * (1 + plus_rate):
                    del globals()[market+'{}'.format('high_price')]
            time.sleep(1)  # if_elif 내부코딩간의진행간격(초)