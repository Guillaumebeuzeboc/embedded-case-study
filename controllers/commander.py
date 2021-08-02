import asyncio
from collections import deque
from collections.abc import Set
from enum import Enum

from .fake_can_library import CAN

ARBITRARY_DURATION = 30

class MessageToSend:
    def __init__(self, address, message = []):
        self.address = address
        self.message = message

class State:
    pass

class StrainerToFlipper(State):
    def to_send(self):
        return None

    def acknowledge(self, msg):
        return  msg == ['0x08', '0x0', '0x0', '0x01']

    def next(self):
        return [OpenWindow(), DropBox()]

class OpenWindow(State):
    def to_send(self):
        return MessageToSend(0x2, ['0x0', '0x0', '0x0', '0x02'])

    def acknowledge(self, msg):
        return msg == ['0x02', '0x0', '0x0', '0x02']

    def next(self):
        return [BringBoxToFlipper()]

class DropBox(State):
    def to_send(self):
        return MessageToSend(0x20, ['0x0', '0x0', '0x0', '0x01'] )
    def acknowledge(self, msg):
        return msg == ['0x20', '0x0', '0x0', '0x01']
    def next(self):
        return [BringBoxToFlipper()]
        
class BringBoxToFlipper(State):
    def to_send(self):
        return MessageToSend(0x04, ['0x0', '0x0', '0x0', '0x02'] )
    def acknowledge(self, msg):
        return msg == ['0x04', '0x0', '0x0', '0x02']
    def next(self):
        return [FlipTheStrainer()]

class FlipTheStrainer(State):
    def to_send(self):
        return MessageToSend(0x04, ['0x0', '0x0', '0x0', '0x01'] )
    def acknowledge(self, msg):
        return msg == ['0x04', '0x0', '0x0', '0x01']
    def next(self):
        return [BoxToAssembler(), ReplaceStrainer()]
    
class ReplaceStrainer(State):
    def to_send(self):
        return MessageToSend(0x08, ['0x0', '0x0', '0x0', '0x02'] )
    def acknowledge(self, msg):
        return msg == ['0x08', '0x0', '0x0', '0x01']
    def next(self):
        return []
    
class BoxToAssembler(State):
    def to_send(self):
        return MessageToSend(0x04, ['0x0', '0x0', '0x0', '0x04'] )
    def acknowledge(self, msg):
        return msg == ['0x04', '0x0', '0x0', '0x04']
    def next(self):
        return [CloseWindow(), BoxToSauce()]
    
class CloseWindow(State):
    def to_send(self):
        return MessageToSend(0x02, ['0x0', '0x0', '0x0', '0x04'] )
    def acknowledge(self, msg):
        return msg == ['0x02', '0x0', '0x0', '0x04']
    def next(self):
        return []
    
class BoxToSauce(State):
    def to_send(self):
        return MessageToSend(0x02, ['0x0', '0x0', '0x0', '0x08'] )
    def acknowledge(self, msg):
        return msg == ['0x04', '0x0', '0x0', '0x08']
    def next(self):
        return []

class Commander:

    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.reception_pcb_messages_queue = deque()
        self.can = CAN(self.reception_pcb_messages_queue)
        self.loop.create_task(self.service())
        self.loop.create_task(self.fake_pcb_message_reception())
        self.states = {StrainerToFlipper()}

    async def call_new_state_msg(self, msg):
        await self.can.send_can_message(msg.address, msg.message)

    async def service(self) -> None:
        print("Main loop")
        # The while below is an example to show you how you receive
        # pcb message when the system has done the task you asked him to do
        while(True):
            await asyncio.sleep(1)
            while self.reception_pcb_messages_queue:
                last_message = self.reception_pcb_messages_queue.pop()
                for state in self.states:
                    if state.acknowledge(last_message['can_message']):
                        self.states.remove(state)
                        # We check the size in order to be sure no
                        if len(self.states) == 0 or all([state.next() == [] for state in self.states]):
                            for new_state in state.next():
                                self.states.add(new_state)
                                self.loop.create_task(self.call_new_state_msg(new_state.to_send()))
                        break
                        

            # Check if message is STRAINER_TO_FLIPPER
            # 
            print(f"{self.reception_pcb_messages_queue}")
            

    async def fake_pcb_message_reception(self) -> None:
        while(True):
            self.reception_pcb_messages_queue.append({
                "system_address": 0x80,
                "can_message": ['0x08', '0x0', '0x0', '0x01']
            })  # STRAINER_TO_FLIPPER
            await asyncio.sleep(ARBITRARY_DURATION)
