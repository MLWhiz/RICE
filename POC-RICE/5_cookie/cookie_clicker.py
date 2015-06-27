"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(200)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        stri = "\n"+"current_cps:"+str(self._current_cps)+",\n"+"current_cookies:"+str(self._current_cookies)+",\n"+"current_time:"+str(self._current_time)+",\n"+"Total_cookies:"+str(self._total_cookies)
        return stri
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        current_cookies=self._current_cookies
        cps = self._current_cps
        time_till = (cookies-current_cookies)/cps
        if time_till<0:
            return 0.0
        else:
            return math.ceil(time_till)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state
        Should do nothing if time <= 0.0
        """
        if time>0:
            self._current_cookies += self._current_cps*time
            self._total_cookies += self._current_cps*time
            self._current_time+=time

    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies-=cost
            self._current_cps+=additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """
    clone_build = build_info.clone()
    game = ClickerState()
    while game.get_time()<=duration:
        item = strategy(game.get_cookies(), game.get_cps(), game.get_history(), duration-game.get_time(), clone_build)
        if item is None:
            game.wait(duration - game.get_time())
            break
        else:
            item_cost = clone_build.get_cost(item)
            item_cps  = clone_build.get_cps(item)
            wait_time = game.time_until(item_cost)
            if game.get_time()+wait_time>duration:
                game.wait(duration - game.get_time())
                break
            else:
                game.wait(wait_time)
                game.buy_item(item, item_cost, item_cps)
                clone_build.update_item(item)

    return game


def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    all_items = build_info.build_items()
    cost = float('inf')
    item_pick = None
    for item in all_items:
        if cost > build_info.get_cost(item):
            cost = build_info.get_cost(item)
            item_pick = item
    if cookies + time_left*cps >= cost:
        return item_pick
    else:
        return None


def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    all_items = build_info.build_items()
    cost = 0
    item_pick = None
    max_cost_allowed = cookies + time_left*cps
    for item in all_items:
        if build_info.get_cost(item)>cost and build_info.get_cost(item)<=max_cost_allowed  :
            cost = build_info.get_cost(item)
            item_pick = item
    
    return item_pick

def strategy_best_calc(item_dict):
    """
    too many local variables
    """

    min_bought =  float('inf')
    min_price  =  float('inf')
    item_pick = None      
    for item,value in item_dict.items():
        num_buy, price = value
        if num_buy<min_bought:
            min_bought = num_buy
            item_pick = item
            min_price = price
        elif num_buy==min_bought:
            if price<min_price:
                item_pick = item
                min_price = price
    return item_pick,min_price

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.Take Item that are never chosen or are chosen very few times
    """
    all_items = build_info.build_items()
    item_dict = {}
    for elem in all_items:
        item_dict[elem]=[0,build_info.get_cost(elem)]
    for value in history:
        _, item_hist , _,_ = value  
        if item_hist is not None:
            num_buy, price = item_dict[item_hist]
            item_dict[item_hist] = [num_buy+1,price]
    
    item_pick,min_price = strategy_best_calc(item_dict)
    if cookies + time_left*cps >= min_price:
        return item_pick
    else:
        return None
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    #run_strategy("Best", SIM_TIME, strategy_best)
    
#run()
#print strategy_expensive(0.0, 1.0, [(0.0, None, 0.0, 0.0)], 5.0, provided.BuildInfo({'A': [5.0, 1.0], 'C': [50000.0, 3.0], 'B': [500.0, 2.0]}, 1.15)) 
print simulate_clicker(provided.BuildInfo({'Cursor': [15.0, 0.10000000000000001]}, 1.15), 15.0,strategy_cursor_broken)     

