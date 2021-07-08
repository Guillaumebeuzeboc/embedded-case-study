import asyncio

from .fake_can_library import CAN

ARBITRARY_DURATION = 30


class Commander:
    def __init__(self) -> None:
        self.loop = asyncio.get_event_loop()
        self.pcb_messages = []
        self.can = CAN(self.pcb_messages)
        self.loop.create_task(self.service())
        self.loop.create_task(self.fake_can_reception())

    async def service(self) -> None:
        print("Main loop")
        while(True):
            await asyncio.sleep(1)
            print(f"{self.pcb_messages}")

    async def fake_can_reception(self) -> None:
        while(True):
            self.pcb_messages.append({
                "system_address": 0x80,
                "can_message": ['0x08', '0x0', '0x0', '0x01']
            })  # STRAINER_IN_FLIPPER
            await asyncio.sleep(ARBITRARY_DURATION)
