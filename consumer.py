"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Thread
from time import sleep

class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """
        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.cart_id = -1
        self.kwargs = kwargs
        self.name = kwargs['name']

    def run(self):
        self.cart_id = self.marketplace.new_cart()
        for cart in self.carts:
            for operation in cart:
                for _ in range(operation['quantity']):
                    op_type = operation['type']
                    product = operation['product']
                    if op_type == 'add':
                        while not self.marketplace.add_to_cart(self.cart_id, product):
                            sleep(self.retry_wait_time)

                    elif op_type == 'remove':
                        self.marketplace.remove_from_cart(self.cart_id, product)

            for product in self.marketplace.place_order(self.cart_id):
                print(f'{self.name} bought {product}')
