import asyncio
from typing import List, Any

from .fake_can_library import CAN

ARBITRARY_DURATION = 30


class Commander:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.reception_pcb_messages_queue = []
        self.can = CAN(self.reception_pcb_messages_queue)
        self.loop.create_task(self.service())
        self.loop.create_task(self.fake_pcb_message_reception())

    async def service(self) -> None:
        print("Main loop")
        # The while below is an example to show you how you receive
        # pcb message when the system has done the task you asked him to do
        while(True):
            await asyncio.sleep(1)
            print(f"{self.reception_pcb_messages_queue}")

    async def fake_pcb_message_reception(self) -> None:
        while(True):
            self.reception_pcb_messages_queue.append({
                "system_address": 0x80,
                "can_message": ['0x08', '0x0', '0x0', '0x01']
            })  # STRAINER_TO_FLIPPER
            await asyncio.sleep(ARBITRARY_DURATION)
