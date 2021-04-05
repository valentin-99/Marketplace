"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

from threading import Lock

class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """
    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.queue_size_per_producer = queue_size_per_producer

        self.prod_id = -1
        self.cart_id = -1

        self.prod_list = []
        self.carts_list = []

        self.mutex = Lock()

    def register_producer(self):
        """
        Returns an id for the producer that calls this.
        """
        with self.mutex:
            self.prod_id += 1
            self.prod_list.append([])
        return self.prod_id

    def publish(self, producer_id, product):
        """
        Adds the product provided by the producer to the marketplace

        :type producer_id: String
        :param producer_id: producer id

        :type product: Product
        :param product: the Product that will be published in the Marketplace

        :returns True or False. If the caller receives False, it should wait and then try again.
        """
        with self.mutex:
            if len(self.prod_list[producer_id]) < self.queue_size_per_producer:
                self.prod_list[producer_id].append((producer_id, product))
                return True
            return False

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        with self.mutex:
            self.cart_id += 1
            self.carts_list.append([])
        return self.cart_id

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        with self.mutex:
            for prod in self.prod_list:
                for p_list in prod:
                    if product == p_list[1]:
                        self.carts_list[cart_id].append(p_list)
                        prod.remove(p_list)
                        return True
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        with self.mutex:
            for prod in self.carts_list[cart_id]:
                if product == prod[1]:
                    self.carts_list[cart_id].remove(prod)
                    self.prod_list[prod[0]].append(prod)
                    break

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        p_list = []
        for prod in self.carts_list[cart_id]:
            p_list.append(prod[1])
        self.carts_list[cart_id] = []
        return p_list
