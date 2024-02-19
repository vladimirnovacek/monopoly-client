from typing import Type

import encoders

server_address = "localhost"
server_port = 8123
encoder: Type[encoders.Encoder] = encoders.PickleEncoder

tokens = [
    "car",
    "hat",
    "thimble",
    "wheelbarrow",
]

# PATHS
path_images = "resources"
path_tokens = "resources/tokens"

# BOARD INFORMATIONS
board_size = {"width": 600, "height": 600}
field_coordinates = [
        (40, 40), (105, 25), (153, 25), (202, 25), (251, 25),
        (299, 25), (348, 25), (397, 25), (445, 25), (494, 25),
        (580, 25), (574, 105), (574, 153), (574, 202), (574, 251),
        (574, 299), (574, 348), (574, 397), (574, 445), (574, 494),
        (559, 559), (494, 574), (445, 574), (397, 574), (348, 574),
        (299, 574), (251, 574), (202, 574), (153, 574), (105, 574),
        (40, 559), (25, 494), (25, 445), (25, 397), (25, 348),
        (25, 299), (25, 251), (25, 202), (25, 153), (25, 105),
        (547, 52)
    ]
dice_location = [(270, 440), (330, 440)]