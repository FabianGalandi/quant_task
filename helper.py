def step(assets, liabilities, value_decline=[0.0, 0.0, 0.0, 0.0]):
    """Make a yearly step, calculating donations, asset value decline, and total assets value after payments 

    Args:
        assets: Dictonary of assets with values
        liabilities: Dictonary of liabilities
        valie_decline: List, 4-tuples of positive floats indicating the relative decline of stocks, bonds, flat in Berlin and flat in Potsdam
    """

    # calculate amount of donations, before this year's asset decline
    liabilities["donations"] = 0.5 * liabilities["donations"] + 0.025 * sum(assets.values())

    # calculate this year's value decline
    assets["stocks"] *= (1-value_decline[0])
    assets["bonds"] *= (1-value_decline[1])
    assets["flat_berlin"] *= (1-value_decline[2])
    assets["flat_potsdam"] *= (1-value_decline[3])

    # calculate payments
    payments = liabilities["donations"] + liabilities["bank_loan"]

    # service payments with shares and bonds depending on their ratio 
    proportion = assets["stocks"] / (assets["stocks"] + assets["bonds"]) # proportion of shares
    assets["stocks"] -= payments*proportion
    assets["bonds"] -= payments*(1-proportion)


def do_three_years(intial_net_asset_value, worst_case_scenario):
    """ Simulate Worst Case Scenario according to the task at hand over the course of three years
    
    Args:
        intial_net_asset_value: Float Amount of initial net asset value
        worst_case_scenario: List, 4-tuples of positive floats indicating the relative decline of stocks, bonds, flat in Berlin and flat in Potsdam

    Return: List as a timeseries with values of each calculated year

    """

    assets = {
        "stocks": intial_net_asset_value * 0.25,
        "bonds": intial_net_asset_value * 0.25,
        "flat_berlin": intial_net_asset_value * 0.25,
        "flat_potsdam": intial_net_asset_value * 0.25}

    liabilities = {
        "donations": 0.05 * sum(assets.values()),
        "bank_loan": (assets["flat_berlin"] + assets["flat_potsdam"]) * 0.1
    }

    timeseries = []

    # append initial values at year=0, nothing has changed
    timeseries.append({"assets": assets.copy(), "liabilities": liabilities.copy(), "scenario": worst_case_scenario})

    for year in range(0,3):

        if(year == 0):
            # only apply value decline of the worst case in first year, as assets neither appreciate or depreciate any further according to task
            step(assets, liabilities, worst_case_scenario)
        else:
            step(assets, liabilities)
        
        timeseries.append({"assets": assets.copy(), "liabilities": liabilities.copy(), "scenario": worst_case_scenario})
    
    return timeseries