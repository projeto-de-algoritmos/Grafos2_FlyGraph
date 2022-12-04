class Response:
    def __init__(self,
                 total_price,
                 num_arestas,
                 total_time,
                 flights=[]):
        
        self.__flights = flights
        self.__total_price = total_price
        self.__num_arestas= num_arestas
        self.__total_time = total_time

   
    @property
    def total_price(self):
        return self.__total_price

    @property
    def total_time(self):
        return self.__total_time

    @property
    def num_arestas(self):
        return self.__num_arestas

    @property
    def flights(self):
        return list(self.__flights)

   

    @total_price.setter
    def oaci(self, total_price):
        self.__total_price = total_price
        
    @total_time.setter
    def oaci(self, total_time):
        self.__total_time = total_time

    @num_arestas.setter
    def num_arestas(self, num_arestas):
        self.__num_arestas = num_arestas
    
    @flights.setter
    def flights(self, flights):
        self.__flights = flights

    def to_dict(self):
        return{
           "flights": [obj.to_dict() for obj in self.flights], 
           "total_price": self.total_price, 
           "num_arestas": self.num_arestas,
           "total_time": self.total_time
        }