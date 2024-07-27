import threading
from threading import Thread
import time
from queue import Queue

class Table:
    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Customer(Thread):
    def __init__(self, number, cafe):
        super().__init__()
        self.number = number
        self.cafe = cafe

    def run(self):
        self.cafe.serve_customer(self)


class Cafe:
    def __init__(self, tables):
        self.queue = Queue()
        self.tables = tables
        self.customer_count = 0

    def customer_arrival(self):
        for customer_number in range(1, 21):
            print(f"Посетитель номер {customer_number} прибыл.")
            customer = Customer(customer_number, self)
            customer.start()
            time.sleep(1)


    def serve_customer(self, customer):
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {customer.number} сел за стол {table.number}')
                time.sleep(5)
                print(f'Посетитель номер {customer.number} покушал и ушел.')
                table.is_busy = False
                if not self.queue.empty():
                    next_customer = self.queue.get()
                    self.serve_customer(next_customer)
                return
        print(f"Посетитель номер {customer.number} ожидает свободный стол.")
        self.queue.put(customer)


table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

cafe = Cafe(tables)

customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)
customer_arrival_thread.start()

customer_arrival_thread.join()

