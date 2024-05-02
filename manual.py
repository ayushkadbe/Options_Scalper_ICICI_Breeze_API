from breeze_connect import BreezeConnect
import login as l


# Initialize SDK
breeze = BreezeConnect(api_key=l.api_key)

def initialize_sdk():
    # Generate Session
    breeze.generate_session(api_secret=l.secret_key,
                            session_token=l.session_key)
#---------------------------------------------------------------------------------
# Connect to websocket(it will connect to tick-by-tick data server)    
def connect_to_socket():
    breeze.ws_connect()
    breeze.subscribe_feeds(get_order_notification=True)   
     
    def on_ticks():
        #Ordebook & Order Status callback to receive ticks
        if('sourceNumber' in ticks.keys()):
            status = ticks['orderStatus']
            order_id = ticks['orderReference']
            action = ticks['orderFlow']
            name = ticks['stockCode'] + ' | ' + ticks['expiryDate'] + ' | ' + ticks['strikePrice'] + ' | ' + ticks['optionType']
            
            print(f"ID : {order_id}\nAction : {action} {name}\nStatus : {status}\n")     #prints only order list
    
    on_ticks == on_ticks
#-----------------------------------------------------------------------------
#Account Data FUNCTIONS
def orderList():
    list = breeze.get_order_list(exchange_code="NSE",
                            from_date="2023-12-01T10:00:00.000Z",
                            to_date="2023-12-10T10:00:00.000Z")
    print(list)
    
def funds():
    fund = breeze.get_funds()
    print(fund)
#---------------------------------------------------------------------------------
#GET ATM PRICE
# stock = 'NIFTY'

def get_atm_strike(stock):
    try:
        spot = breeze.get_quotes(stock_code=stock, exchange_code="NSE")['Success'][0]['ltp'] #get spot value
        atm_strike = 50 * (round(spot / 50))    #Calculate nearest strike price
        print(f"SPOT: {spot} | ATM_STRIKE : {atm_strike}")
        return atm_strike
    except Exception as e:
        print(f"API Error\n{e}\n")
#---------------------------------------------------------------------------------
#GET expiry
def get_expiry_dates(stock, strike):
    try:
        expiry_dates_response = breeze.get_option_chain_quotes(
                                    stock_code=stock.upper(),
                                    exchange_code="NFO",
                                    product_type="options",
                                    expiry_date="",
                                    right="call",
                                    strike_price=strike)
        
        if(expiry_dates_response['Status']==200):
            expiry_dates = [expiry_dates_response['Success'][i]['expiry_date'] for i in range(len)]
            return expiry_dates  #get list of all expiry for given stock and strike
        else:
            print(f'API Error\n{expiry_dates_response}')
    except Exception as e:
        print(f'API Error\n{e}\n')             
        
# expiry_dates = get_expiry_dates("NIFTY", get_atm_strike)
# short_expiry = expiry_dates[0] , long_expiry = expiry_dates[2]
    
#---------------------------------------------------------------------------------
# name = 'NIFTY_28-DEC-2023-23350-CE'
#get_contract(name) => output { get data in dictionary format like stock=, strik= etc}     
# Convert convtract name into dictionary form for api to understand

#Funtion to create a contract
def get_contract(name, action):
    name = name.upper()
    details = name.split('-')
    details[-1] = 'call' if (details[-1] == 'CE') else 'put'
    
    if (details[2].split("/")[1] in ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']):
        expiry = datetime.strftime(details[2], "%d/%b/%Y")
    else:
        expiry = datetime.strftime(details[2], "%d/%m/%Y")
        
    contract = {
        'stock':details[0],
        'strike':details[1],
        'expiry':expiry.strftime('%Y-%m-%dT06:00:00.000Z'),
        'expiry_date':expiry.strftime('%d-%m-%Y'),
        'right': details[-1],
        'name': name,
        'action': action
    }
    return contract
#---------------------------------------------------------------------------------
#Function to generate a signal
def place_order(each_leg):   
    #each_leg input is the Contract/Order generate above
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z') #today's date
    print(f"\nPlacing {each_leg['right']} {each_leg['action']} market order") #order definition: call or put
    
    try:
        #Place options order
        buy_order = breeze.place_order(
                    stock_code= each_leg['stock'],
                    exchange_code="NFO",
                    product="options",
                    action=each_leg['action'],
                    order_type="market",
                    stoploss="",
                    quantity="50",  
                    price="",
                    validity="day",
                    validity_date=today,
                    disclosed_quantity="0",
                    expiry_date=each_leg['expiry'],
                    right=each_leg['right'],
                    strike_price=each_leg['strike'])
        
        #Check if the rest http api request is successful by knowing 'Status' i.e check if order is placed or not
        if(buy_order['Status']==200):
            order_id = buy_order['Success']['order_id']
            print(f'Successfully placed market order !\nOrder ID is {order_id}')
            return order_id
        else:
            print('\nFailed to place order!\n', buy_order['Error'])
            return False
        
    except Exception as error:
        print('Place Order API Error!', error)
        return False    
#---------------------------------------------------------------------------------
#Square off at market price function
def square_off_at_market(each_leg):   
    today = datetime.now().strftime('%Y-%m-%dT06:00:00.000Z') #today's date
    print(f"\nSquaring {each_leg['name']} at market") #order definition: call or put
    
    try:
        #Place square off options order
        sq_off_order = breeze.square_off(exchange_code="NFO",
                    product="options",
                    stock_code=each_leg['stock'],
                    expiry_date=each_leg['expiry'],
                    right=each_leg['right'],
                    strike_price=each_leg['strike'],
                    action="sell",
                    order_type="market",
                    validity="day",
                    stoploss="",
                    quantity="50",
                    price="0",
                    validity_date=today,
                    trade_password="",
                    disclosed_quantity="0")
        
        #Check if the rest http api request is successful by knowing 'Status' i.e check if sq off order is placed or not
        if(buy_order['Status']==200):
            order_id = sq_off_order['Success']['order_id']
            print(sq_off_order)
            return order_id
        else:
            print('\nFailed to square off!\n', sq_off_order['Error'])
            return False
        
    except Exception as error:
        print('Place Order API Error!', error)
        return False    

#---------------------------------------------------------------------------------
#GUI Order Place Code run to perform Scalping 

# DETAILS: MODITY THIS ONLY
# leg_name/contract_name = 'NIFTY-28-DEC-2023-23350-CE' 
# expiry_dates = get_expiry_dates("NIFTY", get_atm_strike)
# short_expiry = expiry_dates[0] , long_expiry = expiry_dates[2]
# expiry_dates = get_expiry_dates(stock, strike)
# current_expiry = expiry_dates[0]

stock = 'NIFTY'
strike = get_atm_strike(stock)
call_leg = 'NIFTY-'+ strike+'-28-DEC-2023-CE'

put_leg = 'NIFTY-21600-28/dec/2023-PE'
cx = get_contract(put_leg, 'buy')
print(cx)
place_order(cx)
square_off_at_market(cx)

place_order(get_contract(put_leg,'buy'))

square_off_at_market(get_contract(call_leg,'buy'))    

sqyare_off_at_market(get_contract(put_leg,'buy'))    
        
