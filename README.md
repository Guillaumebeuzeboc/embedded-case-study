# Embedded-case-study

This repository is to reproduce CAN communication between the Raspberry Pi (sometimes called Robot) and the micro-controllers on PCB representing systems. This part is what we call the Commander, it's hosted in the Rasberry Pi in the robot, managing the scheduled actions of meals creation.

The robot systems are:

- Box
- Assembler
- Sampling
- Cooking zone
- Sauce
- TER (bringing pasta out of the robot to the food team)

The code is in Python and use AsyncIO to manage infinite loop and async requests.

## Requirements

- Python >= 3.7

## Instructions

The goal of this case study is to reproduce the sequence (the picture below) sending CAN message needed to prepare a dish depending on requeriements. A task receiving an arrow on the sequence needs to wait for the end of the previous task to be started let's call it a requirement. A task can have more than 1 requirement like the BRING_BOX_TO_FLIPPER, so you will have to wait for all the requirements acknowledgement to start this task.
In your case you are in charge of a part of meal creation, that's why the sequence is short. You will receive STRAINER_TO_FLIPPER acknowledgement message every ARBITRARY_DURATION's value (stored in commander file) from the system Arm and you will have to manage all the tasks until BOX_TO_SAUCE.
Print the can message you send and the acknowlegement you receive in the format

`Message sent from {system} data: {can_message}`

`Message recieved data: {acknowledgement}`

CAN messages and aknowledgement are array of 4 hexadecimal values

You will have to:

- fork this project to work on it
- reproduce the sequence sending can message and waiting for their acknowledgement.
- create a system adaptable to additionnal systems
- create a system time efficient

## Development

Install dependencies

```bash
pip3 install requirements.txt
```

Start the project

```bash
python3 main.py
```

## Sequences

![case-study](https://user-images.githubusercontent.com/8608444/124930553-b8814200-e001-11eb-887b-4894c665a88c.jpeg)

## Assembler

System code: 0x02

### Assembler Can messages

| Name         | message[0] | message[1] | message[2] | message[3] |
| ------------ | ---------- | ---------- | ---------- | ---------- |
| OPEN_WINDOW  | 0          | 0          | 0          | 2          |
| CLOSE_WINDOW | 0          | 0          | 0          | 4          |

### Assembler Acknowledgements

| Name         | message[0] | message[1] | message[2] | message[3] |
| ------------ | ---------- | ---------- | ---------- | ---------- |
| OPEN_WINDOW  | 2          | 0          | 0          | 2          |
| CLOSE_WINDOW | 2          | 0          | 0          | 4          |

## Cooking zone

System code: 0x04

### Cooking zone Can messages

| Name                 | message[0] | message[1] | message[2] | message[3] |
| -------------------- | ---------- | ---------- | ---------- | ---------- |
| FLIP_THE_STRAINER    | 0          | 0          | 0          | 1          |
| BRING_BOX_TO_FLIPPER | 0          | 0          | 0          | 2          |
| BOX_TO_ASSEMBLER     | 0          | 0          | 0          | 4          |
| BOX_TO_SAUCE         | 0          | 0          | 0          | 8          |

### Cooking zone Acknowledgements

| Name                 | message[0] | message[1] | message[2] | message[3] |
| -------------------- | ---------- | ---------- | ---------- | ---------- |
| FLIP_THE_STRAINER    | 4          | 0          | 0          | 1          |
| BRING_BOX_TO_FLIPPER | 4          | 0          | 0          | 2          |
| BOX_TO_ASSEMBLER     | 4          | 0          | 0          | 4          |
| BOX_TO_SAUCE         | 4          | 0          | 0          | 8          |

## Arm

System code: 0x08

### Arm can messages

| Name                | message[0] | message[1] | message[2] | message[3] |
| ------------------- | ---------- | ---------- | ---------- | ---------- |
| STRAINER_TO_FLIPPER | 0          | 0          | 0          | 1          |
| REPLACE_STRAINER    | 0          | 0          | 0          | 2          |

### Arm Acknowledgements

| Name                | message[0] | message[1] | message[2] | message[3] |
| ------------------- | ---------- | ---------- | ---------- | ---------- |
| STRAINER_TO_FLIPPER | 8          | 0          | 0          | 1          |
| REPLACE_STRAINER    | 8          | 0          | 0          | 2          |

## Box

System code: 0x20

### Box can messages

| Name     | message[0] | message[1] | message[2] | message[3] |
| -------- | ---------- | ---------- | ---------- | ---------- |
| DROP_BOX | 0          | 0          | 0          | 1          |

### Box Acknowledgements

| Name     | message[0] | message[1] | message[2] | message[3] |
| -------- | ---------- | ---------- | ---------- | ---------- |
| DROP_BOX | 20         | 0          | 0          | 1          |
