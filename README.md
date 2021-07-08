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
In your case you are in charge of a part of meal creation, that's why the sequence is short. You will receive STRAINER_TO_FLIPPER from the system Arm and you will have to manage all the tasks until BOX_TO_SAUCE.

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

## Can messages

Can messages are array of hex numbers

| Name                 | message[0] | message[1] | message[2] | message[3] | system_code | acknowledgement[0] | acknowledgement[1] | acknowledgement[2] | acknowledgement[3] |
| -------------------- | ---------- | ---------- | ---------- | ---------- | ----------- | ------------------ | ------------------ | ------------------ | ------------------ |
| OPEN_WINDOW          | 0          | 0          | 0          | 2          | 2           | 2                  | 0                  | 0                  | 2                  |
| CLOSE_WINDOW         | 0          | 0          | 0          | 4          | 2           | 2                  | 0                  | 0                  | 4                  |
| FLIP_THE_STRAINER    | 0          | 0          | 0          | 1          | 4           | 4                  | 0                  | 0                  | 1                  |
| BRING_BOX_TO_FLIPPER | 0          | 0          | 0          | 2          | 4           | 4                  | 0                  | 0                  | 2                  |
| BOX_TO_ASSEMBLER     | 0          | 0          | 0          | 4          | 4           | 4                  | 0                  | 0                  | 4                  |
| BOX_TO_SAUCE         | 0          | 0          | 0          | 8          | 4           | 4                  | 0                  | 0                  | 8                  |
| STRAINER_TO_FLIPPER  | 0          | 0          | 0          | 1          | 8           | 8                  | 0                  | 0                  | 1                  |
| REPLACE_STRAINER     | 0          | 0          | 0          | 2          | 8           | 8                  | 0                  | 0                  | 2                  |
| DROP_BOX             | 0          | 0          | 0          | 1          | 20          | 20                 | 0                  | 0                  | 1                  |
