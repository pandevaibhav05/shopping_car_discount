"""Calculate total final price of items in cart after applying discount if required"""
__author__ = "Vaibhav Pande"

from datetime import date


def final_coffee_price_after_discount():
    """Return number of coffee bags if offer applicable"""
    num_of_items = PRODUCTS_DICT["CF1"]["final_count"]
    if num_of_items % 2 == 0:
        return (num_of_items/2) * PRODUCTS_DICT["CF1"]["price"]
    else:
        return ((num_of_items / 2) + 1) * PRODUCTS_DICT["CF1"]["price"]


def final_price_per_apple_bag(num_of_apples, actual_price):
    """Return discounted price if offer applicable"""
    if num_of_apples >= 3:
        return float("4.50")
    return actual_price


def final_price_of_milk(chai_count, final_milk_price):
    """Return discounted price if offer applicable"""
    if chai_count:
        # Only 1 milk packet free on one or more chai bags
        final_milk_price = final_milk_price - PRODUCTS_DICT["MK1"]["price"]
    return final_milk_price


def final_price_of_apple_bags(oat_bag_count, apple_bag_count):
    """Return final price if offer applicable"""
    if oat_bag_count >= apple_bag_count:
        return apple_bag_count * PRODUCTS_DICT["AP1"]["price"] * 0.5
    else:
        discounted_bags = apple_bag_count - oat_bag_count
        actual_count_bags = apple_bag_count - discounted_bags
        return (discounted_bags * PRODUCTS_DICT["AP1"]["price"] * 0.5) + \
               (actual_count_bags * PRODUCTS_DICT["AP1"]["price"])


PRODUCTS_DICT = {
    "CH1": {
        "name": "Chai",
        "price": float("3.11"),
        "final_count": 0
    },
    "AP1": {
        "name": "Apples",
        "price": float("6.00"),
        "price_calculation_method": [final_price_per_apple_bag, final_price_of_apple_bags],
        "final_count": 0
    },

    "CF1": {
        "name": "Coffee",
        "price": float("11.23"),
        "price_calculation_method": final_coffee_price_after_discount,
        "final_count": 0
    },
    "MK1": {
        "name": "Milk",
        "price": float("4.75"),
        "final_count": 0,
        "price_calculation_method": final_price_of_milk
    },
    "OM1": {
        "name": "Oatmeal",
        "price": float("3.69"),
        "final_count": 0

    }
}


def check_wrong_input(item_list):
    for item in list(item_list):
        if item not in PRODUCTS_DICT:
            item_list.remove(item)
    print(item_list)


def print_final_checkout_price(item_list):
    first_day = date(year=2021, month=4, day=5)
    last_day = date(year=2021, month=4, day=11)
    offer_applicable = first_day <= date.today() <= last_day
    for item in item_list:
        PRODUCTS_DICT[item]['final_count'] += 1

    final_item_set = set(item_list)
    final_cart_price = 0

    for item in final_item_set:
        if item == "AP1" and offer_applicable:
            # call final_price_per_apple
            final_price_per_item = PRODUCTS_DICT[item]["price_calculation_method"][0]\
                (PRODUCTS_DICT[item]['final_count'], PRODUCTS_DICT[item]["price"])
            final_item_price = PRODUCTS_DICT[item]['final_count'] * final_price_per_item
            # Check if oatmeal is in cart and calculate discounted price accordingly, call final_price_of_apple_bags
            if "OM1" in final_item_set:
                final_item_price2 = PRODUCTS_DICT[item]["price_calculation_method"][1](PRODUCTS_DICT["OM1"]["final_count"],PRODUCTS_DICT[item]["final_count"])
                # Consider least price after applying both discount to consider final price
                final_item_price = final_item_price if final_item_price < final_item_price2 else final_item_price2
        elif item == "MK1" and offer_applicable:
            final_item_price = PRODUCTS_DICT[item]['final_count'] * PRODUCTS_DICT[item]["price"]
            final_item_price = PRODUCTS_DICT[item]["price_calculation_method"](PRODUCTS_DICT["CH1"]["final_count"], final_item_price)
        elif item == "CF1" and offer_applicable:
            final_item_price = PRODUCTS_DICT[item]["price_calculation_method"]()
        else:
            final_item_price = PRODUCTS_DICT[item]['final_count'] * PRODUCTS_DICT[item]["price"]
        final_cart_price += final_item_price
    print("Total price expected: $" + str(final_cart_price))

# Take input form console e.g. "CH1, AP1, AP1, AP1, MK1"
input_args = str(input())

# create list of all items in cart
item_list = [item.strip() for item in input_args.split(",")]
# check and rectify for incorrect items in list
check_wrong_input(item_list)

# calculate and print final cart price
print_final_checkout_price(item_list)


