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
path_cards = "resources/cards"

# BOARD INFORMATIONS
board_size = {"width": 600, "height": 600}
token_field_positions = [
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
field_coordinates = [  # NW corner, SE corner
    ((0, 0), (78, 79)),  # Go
    ((78, 0), (126, 79)),  # brown_1
    ((126, 0), (175, 79)),  # cc_1
    ((175, 0), (224, 79)),  # brown_2
    ((224, 0), (273, 79)),  # tax_1
    ((273, 0), (323, 79)),  # rr_1
    ((323, 0), (372, 79)),  # lblue_1
    ((372, 0), (421, 79)),  # chance_1
    ((421, 0), (470, 79)),  # lblue_2
    ((470, 0), (519, 79)),  # lblue_3
    ((575, 0), (599, 79)),  # just_visiting
    ((519, 79), (599, 128)),  # purple_1
    ((519, 128), (599, 177)),  # utility_1
    ((519, 177), (599, 226)),  # purple_2
    ((519, 226), (599, 275)),  # purple_3
    ((519, 275), (599, 324)),  # rr_2
    ((519, 324), (599, 373)),  # orange_1
    ((519, 373), (599, 422)),  # cc_2
    ((519, 422), (599, 471)),  # orange_2
    ((519, 471), (599, 520)),  # orange_3
    ((519, 520), (599, 599)),  # parking
    ((470, 520), (519, 599)),  # red_1
    ((421, 520), (470, 599)),  # chance_2
    ((372, 520), (421, 599)),  # red_2
    ((323, 520), (372, 599)),  # red_3
    ((273, 520), (323, 599)),  # rr_3
    ((225, 520), (273, 599)),  # yellow_1
    ((175, 520), (225, 599)),  # yellow_2
    ((127, 520), (175, 599)),  # utility_2
    ((78, 520), (127, 599)),  # yellow_3
    ((0, 520), (78, 599)),  # go_to_jail
    ((0, 471), (78, 520)),  # green_1
    ((0, 421), (78, 471)),  # green_2
    ((0, 372), (78, 421)),  # cc_3
    ((0, 323), (78, 372)),  # green_3
    ((0, 273), (78, 323)),  # rr_4
    ((0, 224), (78, 273)),  # chance_3
    ((0, 175), (78, 224)),  # dblue_1
    ((0, 126), (78, 175)),  # tax_2
    ((0, 78), (78, 126)),  # dblue_2
    ((519, 22), (575, 79))  # jail
]
dice_location = [(270, 440), (330, 440)]
