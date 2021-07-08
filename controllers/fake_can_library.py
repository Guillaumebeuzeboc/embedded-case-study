import asyncio
from typing import List, Optional, Any


class CAN:
    def __init__(self, pcb_messages: dict[str, Any]) -> None:
        self.pcb_messages = pcb_messages
        self.messages = [
            {
                "system_code": 0x02,
                "can": ['0x0', '0x0', '0x0', '0x02'],
                "acknowledgement": ['0x02', '0x0', '0x0', '0x02']
            },
            {
                "system_code": 0x20,
                "can": ['0x0', '0x0', '0x0', '0x01'],
                "acknowledgement": ['0x20', '0x0', '0x0', '0x01']
            },
            {
                "system_code": 0x08,
                "can": ['0x0', '0x0', '0x0', '0x01'],
                "acknowledgement": ['0x08', '0x0', '0x0', '0x01']
            },
            {
                "system_code": 0x04,
                "can": ['0x0', '0x0', '0x0', '0x02'],
                "acknowledgement": ['0x04', '0x0', '0x0', '0x08']
            },
            {
                "system_code": 0x02,
                "can": ['0x0', '0x0', '0x0', '0x01'],
                "acknowledgement": ['0x02', '0x0', '0x0', '0x01']
            },
            {
                "system_code": 0x04,
                "can": ['0x0', '0x0', '0x0', '0x04'],
                "acknowledgement": ['0x0', '0x0', '0x0', '0x04']
            },
            {
                "system_code": 0x04,
                "can": ['0x0', '0x0', '0x01', 'x01'],
                "acknowledgement": ['0x04', '0x0', '0x01', '0x01']
            },
            {
                "system_code": 0x08,
                "can": ['0x0', '0x0', '0x0', '0x02'],
                "acknowledgement": ['0x08', '0x0', '0x0', '0x02']
            },
            {
                "system_code": 0x02,
                "can": ['0x0', '0x0', '0x0', '0x04'],
                "acknowledgement": ['0x02', '0x0', '0x0', '0x04']
            }
        ]

    def __del__(_) -> None:
        print("Can service destroyed")

    def get_system_name_from_code(_, system_code: int) -> str:
        if system_code == 0x02:
            return 'Cooking zone'
        if system_code == 0x04:
            return 'Assembler'
        if system_code == 0x08:
            return 'Arm'
        if system_code == 0x20:
            return 'Box'
        if system_code == 0x80:
            return 'Pi'

    # Fake can function returning acknowledgement if found and nothing if the combo message and system is unknown
    async def send_can_message(self, system_address: int, can_message: List[str]) -> Optional[dict[str, Any]]:
        for message in self.messages:
            if message["can"] == can_message and system_address == message["system_code"]:
                print(
                    f"Can message sent {message['can']} sent to {self.get_system_name_from_code(system_address)}")
                await asyncio.sleep(2)
                self.pcb_messages.append({
                    "system_address": 0x80,
                    "can_message": message['acknowledgement']
                })
        return None
