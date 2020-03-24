from abc import abstractmethod, ABCMeta 
import datetime 
try:
    import Queue as queue 
except ImportError :
    import queue 
from event import FillEvent, OrderEvent 

class ExecutionHandler(object):
    __metaclass__=ABCMeta #메타클래스 : 클래스를 만들어내는 클래스.(클래스는 보통 객체를 만들어낸다)
    #사실 type()이 메타클래스의 역할을 수행하기도 한다. 동적으로 클래스를 만들기 위해 필요하다.
    #메타클래스를 직접 지목하면, 해당 방법으로 Execu...클래스를 생성한다. 지정안하면 type을 이용한다.

    @abstractmethod
    def execute_order(self,event):
        raise NotImplementedError('should implement execute_order()')

class SimulatedExecutionHandler(ExecutionHandler):
    def __init__(self,events): #events는 queue클래스의 인스턴스가 될 것이다. 그래서 .put()메서드가 있다.
        self.events=events 
    def execute_order(self,event):
        if event.type=='ORDER':
            fill_event=FillEvent(datetime.datetime.utcnow(),event.symbol,'ARCA',event.qunatity,event.direction,None)
            self.events.put(fill_event)