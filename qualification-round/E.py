import heapq
from abc import ABC, abstractmethod


class Request(ABC):
    def __init__(self, id: int, price: float, volume: int):
        self.id = id
        self.price = price
        self.volume = volume

    @abstractmethod
    def req_type(self) -> str:
        raise NotImplemented()

    def __str__(self):
        return f"{self.id} {self.req_type()} {self.price:.2f} {self.volume}"

    @staticmethod
    def key(r: "Request") -> tuple[float, int]:
        if r.req_type() == "BUY":
            return r.price, -r.id
        return r.price, r.id


class BuyRequest(Request):
    def req_type(self) -> str:
        return "BUY"

    def __lt__(self, other: "BuyRequest"):
        return (self.price, -self.id) > (other.price, -other.id)


class SellRequest(Request):
    def req_type(self) -> str:
        return "SELL"

    def __lt__(self, other: "SellRequest"):
        return (self.price, self.id) < (other.price, other.id)


class Operation:
    def __init__(self, buy_id: int, sell_id: int, price: float, volume: int):
        self.buy_id = buy_id
        self.sell_id = sell_id
        self.price = price
        self.volume = volume

    def __str__(self):
        return f"{self.buy_id} {self.sell_id} {self.price:.2f} {self.volume}"


class StockManager:
    def __init__(self):
        self.ids_seq = 1
        self.buy_requests: list[BuyRequest] = []
        self.sell_requests: list[SellRequest] = []
        self.deleted_request_ids: set[int] = set()
        self.operations_log: list[Operation] = []

    def add_buy_request(self, price: float, volume: int) -> int:
        buy_req = BuyRequest(self.ids_seq, price, volume)
        self.ids_seq += 1
        while buy_req.volume > 0 and len(self.sell_requests) > 0 and self.sell_requests[0].price <= price:
            sell_req = self.sell_requests[0]
            if sell_req.id in self.deleted_request_ids:
                heapq.heappop(self.sell_requests)
                continue
            deal_volume = min(sell_req.volume, buy_req.volume)
            if buy_req.volume >= sell_req.volume:
                heapq.heappop(self.sell_requests)
                self.deleted_request_ids.add(sell_req.id)
            else:
                sell_req.volume -= buy_req.volume
                self.deleted_request_ids.add(buy_req.id)
            self.operations_log.append(Operation(buy_req.id, sell_req.id, sell_req.price, deal_volume))
            buy_req.volume -= deal_volume
        if buy_req.volume > 0:
            heapq.heappush(self.buy_requests, buy_req)
        return buy_req.id

    def add_sell_request(self, price: float, volume: int) -> int:
        sell_req = SellRequest(self.ids_seq, price, volume)
        self.ids_seq += 1
        while sell_req.volume > 0 and len(self.buy_requests) > 0 and self.buy_requests[0].price >= price:
            buy_req = self.buy_requests[0]
            if buy_req.id in self.deleted_request_ids:
                heapq.heappop(self.buy_requests)
                continue
            deal_volume = min(sell_req.volume, buy_req.volume)
            if sell_req.volume >= buy_req.volume:
                heapq.heappop(self.buy_requests)
                self.deleted_request_ids.add(buy_req.id)
            else:
                buy_req.volume -= sell_req.volume
                self.deleted_request_ids.add(sell_req.id)
            self.operations_log.append(Operation(buy_req.id, sell_req.id, sell_req.price, deal_volume))
            sell_req.volume -= deal_volume
        if sell_req.volume > 0:
            heapq.heappush(self.sell_requests, sell_req)
        return sell_req.id

    def delete_request(self, id: int) -> bool:
        if id >= self.ids_seq or id in self.deleted_request_ids:
            return False
        self.deleted_request_ids.add(id)
        return True

    def get_operations(self, count: int) -> list[Operation]:
        return self.operations_log[-min(count, len(self.operations_log)):]

    def get_requests(self) -> list[Request]:
        requests: list[Request] = []
        for buy_req in self.buy_requests:
            if buy_req.id in self.deleted_request_ids:
                continue
            requests.append(buy_req)
        for sell_req in self.sell_requests:
            if sell_req.id in self.deleted_request_ids:
                continue
            requests.append(sell_req)
        requests.sort(key=Request.key, reverse=True)
        return requests


def process_requests():
    sm = StockManager()
    n = int(input())
    for _ in range(n):
        query = input().split()
        if query[0] == "ADD":
            price, volume = float(query[2]), int(query[3])
            if query[1] == "BUY":
                print(sm.add_buy_request(price, volume))
            else:
                print(sm.add_sell_request(price, volume))
            continue
        if query[0] == "GET":
            for req in sm.get_requests():
                print(req)
            continue
        if query[0] == "DELETE":
            if sm.delete_request(int(query[1])):
                print("DELETED")
            else:
                print("NOT FOUND")
            continue
        if query[0] == "SHOW_OPERATIONS":
            for op in sm.get_operations(int(query[1])):
                print(op)


process_requests()
