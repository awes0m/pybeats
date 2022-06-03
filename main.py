import pygame as pg
from pygame import mixer


# initialize pygame
pg.init()

# DISPLAY SIZE
WIDTH = 1366
HEIGHT = 710

# COLORS
black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
dark_gray = (64, 64, 64)
light_gray = (170, 170, 170)


# load in sounds
hi_hat = mixer.Sound("./assets/sounds/hi hat.wav")
snare = mixer.Sound("./assets/sounds/snare.wav")
kick = mixer.Sound("./assets/sounds/kick.wav")
crash = mixer.Sound("./assets/sounds/crash.wav")
clap = mixer.Sound("./assets/sounds/clap.wav")
tom = mixer.Sound("./assets/sounds/tom.WAV")


## Initial Screen info ##
screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Py Beats")
label_font = pg.font.SysFont("Ariel", 35, bold=pg.font.Font.bold)
medium_font = pg.font.SysFont("Ariel", 25)
# label_font = pg.font.SysFont( "assets/Roboto-Bold.ttf", 3050, bold=pg.font.Font.bold)

# initialize variables
index = 100
fps = 60
"""Frames processing per second- lower for better performance"""
timer = pg.time.Clock()
"""clock"""
beats = 8
"""Beats per loop:int"""
instruments = 6
"""Number of Drum Instruments:int"""
bpm = 240
"""Beats per minute- controls speed of looping the sound"""
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
pg.mixer.set_num_channels(instruments * 4)

playing = True
"""Boolean to determine whether or not the loop is playing, controlled by the play button"""
active_length = 0
active_beat = 1
"""The active beat is the beat that is currently being played"""
beat_changed = True

save_menu = False
"""Controls save menu open/close"""
load_menu = False
"""Controls the load menu"""
saved_beats = []
file = open("saved_beats.txt", "r+")
for line in file:
    saved_beats.append(line)
# saved_beats.extend(iter(file))

beat_name = ""
typing = False


def draw_grid(clicks, beat, actives):
    """
    The draw_grid function draws the grid of buttons and lines that will be used to play back the music.
    It takes in a list of clicks, which is a list containing lists for each instrument. Each inner list contains integers
    representing beats where -2 represents an inactive beat, -3 represents an active but not clicked beat,

    :param clicks: Store the state of each instrument
    :param beat: Determine which beat is currently being played
    :param actives: Determine which instrument is active
    :return: A list of rectangles and their coordinatest
    """

    # left_box = pg.draw.rect(screen,white , [0, 0, 200, HEIGHT])
    left_box_outline = pg.draw.rect(screen, gray, [0, 0, 200, HEIGHT], 5)
    bottom_panel = pg.draw.rect(screen, black, [0, HEIGHT - 120, WIDTH, 120])
    bottom_panel_outline = pg.draw.rect(screen, gray, [0, HEIGHT - 120, WIDTH, 120], 12)
    for i in range(instruments + 1):
        pg.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)
    boxes = []
    colors = [gray, white, gray]
    hi_hat_text = label_font.render("Hi Hat", True, colors[actives[0]])
    screen.blit(hi_hat_text, (30, 30))
    snare_text = label_font.render("Snare", True, colors[actives[1]])
    screen.blit(snare_text, (30, 130))
    kick_text = label_font.render("kick", True, colors[actives[2]])
    screen.blit(kick_text, (30, 230))
    crash_text = label_font.render("Crash", True, colors[actives[3]])
    screen.blit(crash_text, (30, 330))
    clap_text = label_font.render("Clap", True, colors[actives[4]])
    screen.blit(clap_text, (30, 430))
    floorTom_text = label_font.render("Floor Tom", True, colors[actives[5]])
    screen.blit(floorTom_text, (30, 530))

    for i in range(beats):
        for j in range(instruments):
            if clicks[j][i] == -1:
                color = gray
            else:
                color = green if actives[j] == 1 else dark_gray

            rect = pg.draw.rect(
                screen,
                color,
                [
                    i * ((WIDTH - 200) // beats) + 205,
                    (j * 100) + 5,
                    ((WIDTH - 200) // beats) - 10,
                    ((HEIGHT - 200) // instruments) - 10,
                ],
                0,
                3,
            )

            pg.draw.rect(
                screen,
                gold,
                [
                    i * ((WIDTH - 200) // beats) + 200,
                    (j * 100),
                    ((WIDTH - 200) // beats),
                    ((HEIGHT - 200) // instruments),
                ],
                5,
                5,
            )
            pg.draw.rect(
                screen,
                black,
                [
                    i * ((WIDTH - 200) // beats) + 200,
                    (j * 100),
                    ((WIDTH - 200) // beats),
                    ((HEIGHT - 200) // instruments),
                ],
                2,
                5,
            )
            boxes.append((rect, (i, j)))
        active = pg.draw.rect(
            screen,
            blue,
            [
                beat * ((WIDTH - 200) // beats) + 200,
                0,
                ((WIDTH - 200) // beats),
                instruments * 100 - 15,
            ],
            5,
            3,
        )
    return boxes


def play_notes():
    """
    The play_notes function plays the notes that are clicked on.
    It loops through all of the active_list and clicks on any note that is active.

    :return: None
    """

    for i in range(len(clicked)):
        if clicked[i][active_beat] == 1 and active_list[i] == 1:
            if i == 0:
                hi_hat.play()
            elif i == 1:
                snare.play()
            elif i == 2:
                kick.play()
            elif i == 3:
                crash.play()
            elif i == 4:
                clap.play()
            elif i == 5:
                tom.play()


## SCREENS ##


def draw_save_menu(beat_name, typing):
    """
    The draw_save_menu function draws the save menu onto the screen. It draws a black rectangle over
    the entire screen, then draws two buttons on top of it. The first button is to exit out of this menu,
    and the second button is to save and close out of this menu.

    :param beat_name: Store the name of the beat that is being saved
    :param typing: Determine whether or not the user is typing in a name for their beat
    :return: The exit_btn, saving_btn, and entry_rect

    """
    pg.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render("SAVE MENU: Enter a Name for this beat", True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pg.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    saving_btn = pg.draw.rect(
        screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.75, 200, 100], 0, 5
    )
    saving_text = label_font.render("Save Beat", True, white)
    screen.blit(saving_text, (WIDTH // 2 - 70, HEIGHT * 0.75 + 30))
    if typing:
        pg.draw.rect(screen, dark_gray, [400, 200, 600, 200], 0, 5)
    entry_rect = pg.draw.rect(screen, gray, [400, 200, 600, 200], 5, 5)
    entry_text = label_font.render(f"{beat_name}", True, white)
    screen.blit(entry_text, (430, 250))
    return exit_btn, saving_btn, beat_name, entry_rect


def draw_load_menu(index):
    """
    The draw_load_menu function draws the load menu on the screen. It draws a black rectangle over
    the entire screen, then draws a gray box with rounded corners to cover all of the beats except for
    the one that is selected by the user. The function also displays text in white font inside of this
    box, including beat

    :param index: Determine which row is selected in the load menu
    :return: A list of the loaded beat's information
    :doc-author: Trelent
    """

    loaded_clicked = []
    loaded_beats = 0
    loaded_bpm = 0
    pg.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render("LOAD MENU: Select a beat to load in", True, white)
    screen.blit(menu_text, (400, 40))
    exit_btn = pg.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90], 0, 5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 160, HEIGHT - 70))
    loading_btn = pg.draw.rect(
        screen, gray, [WIDTH // 2 - 100, HEIGHT * 0.87, 200, 100], 0, 5
    )
    loading_text = label_font.render("Load Beat", True, white)
    screen.blit(loading_text, (WIDTH // 2 - 70, HEIGHT * 0.87 + 30))
    delete_btn = pg.draw.rect(
        screen, gray, [WIDTH // 2 - 400, HEIGHT * 0.87, 200, 100], 0, 5
    )
    delete_text = label_font.render("Delete Beat", True, white)
    screen.blit(delete_text, (WIDTH // 2 - 385, HEIGHT * 0.87 + 30))
    if 0 <= index < len(saved_beats):
        pg.draw.rect(screen, light_gray, [190, 100 + index * 50, 1000, 50])
    for beat in range(len(saved_beats)):
        if beat < 10:
            beat_clicked = []
            row_text = medium_font.render(f"{beat + 1}", True, white)
            screen.blit(row_text, (200, 100 + beat * 50))
            name_index_start = saved_beats[beat].find("name: ") + 6
            name_index_end = saved_beats[beat].find(", beats:")
            name_text = medium_font.render(
                saved_beats[beat][name_index_start:name_index_end], True, white
            )
            screen.blit(name_text, (240, 100 + beat * 50))
        if 0 <= index < len(saved_beats) and beat == index:
            beats_index_end = saved_beats[beat].index(", bpm:")
            loaded_beats = int(saved_beats[beat][name_index_end + 8 : beats_index_end])
            bpm_index_end = saved_beats[beat].index(", selected:")
            loaded_bpm = int(saved_beats[beat][beats_index_end + 6 : bpm_index_end])
            loaded_clicks_string = saved_beats[beat][bpm_index_end + 14 : -3]
            loaded_clicks_rows = list(loaded_clicks_string.split("], ["))
            for row in range(len(loaded_clicks_rows)):
                loaded_clicks_row = loaded_clicks_rows[row].split(", ")
                for item in range(len(loaded_clicks_row)):
                    if (
                        loaded_clicks_row[item] == "1"
                        or loaded_clicks_row[item] == "-1"
                    ):
                        loaded_clicks_row[item] = int(loaded_clicks_row[item])
                beat_clicked.append(loaded_clicks_row)
                loaded_clicked = beat_clicked
    loaded_info = [loaded_beats, loaded_bpm, loaded_clicked]
    entry_rect = pg.draw.rect(screen, gray, [190, 90, 1000, 400], 5, 5)
    return exit_btn, loading_btn, entry_rect, delete_btn, loaded_info


# MAIN LOOP #
run = True
while run:
    # DRAWING SCREEN
    timer.tick(fps)
    screen.fill(black)

    boxes = draw_grid(clicked, active_beat, active_list)

    # lower menu buttons
    play_pause_button = pg.draw.rect(screen, gray, [50, HEIGHT - 100, 100, 80], 0, 5)
    play_text = label_font.render("Play", True, gold if playing else dark_gray)
    screen.blit(play_text, (70, HEIGHT - 80))
    if playing:
        play_text2 = medium_font.render("Playing", True, green)
    else:
        play_text2 = medium_font.render("Paused", True, red)

    screen.blit(play_text2, (64, HEIGHT - 50))

    ## BPM Stuff
    bpm_rect = pg.draw.rect(screen, gray, [170, HEIGHT - 100, 170, 80], 5, 5)
    bpm_text = medium_font.render("Beats Per Minute", True, white)
    screen.blit(bpm_text, (185, HEIGHT - 85))
    bpm_text2 = label_font.render(f"{bpm}", True, white)
    screen.blit(bpm_text2, (230, HEIGHT - 55))
    bpm_add_rect = pg.draw.rect(screen, gray, [350, HEIGHT - 100, 48, 37], 0, 5)
    bpm_sub_rect = pg.draw.rect(screen, gray, [350, HEIGHT - 60, 48, 37], 0, 5)
    add_text = medium_font.render("+5", True, white)
    sub_text = medium_font.render("-5", True, white)
    screen.blit(add_text, (366, HEIGHT - 87))
    screen.blit(sub_text, (366, HEIGHT - 47))

    ## Beats Stuff
    beats_rect = pg.draw.rect(screen, gray, [420, HEIGHT - 100, 170, 80], 5, 5)
    beats_text = medium_font.render("Beats in Loop", True, white)
    screen.blit(beats_text, (450, HEIGHT - 85))
    beats_text2 = label_font.render(f"{beats}", True, white)
    screen.blit(beats_text2, (500, HEIGHT - 55))
    beats_add_rect = pg.draw.rect(screen, gray, [600, HEIGHT - 100, 48, 37], 0, 5)
    beats_sub_rect = pg.draw.rect(screen, gray, [600, HEIGHT - 60, 48, 37], 0, 5)
    add_text = medium_font.render("+1", True, white)
    sub_text = medium_font.render("-1", True, white)
    screen.blit(add_text, (616, HEIGHT - 87))
    screen.blit(sub_text, (616, HEIGHT - 47))

    # save and load buttons
    save_button = pg.draw.rect(screen, gray, [700, HEIGHT - 100, 200, 37], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (720, HEIGHT - 90))
    load_button = pg.draw.rect(screen, gray, [700, HEIGHT - 60, 200, 37], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (720, HEIGHT - 50))

    # clear_button
    clear_button = pg.draw.rect(screen, gray, [950, HEIGHT - 80, 200, 40], 0, 5)
    clear_text = label_font.render("Clear Board", True, black)
    screen.blit(clear_text, (970, HEIGHT - 70))

    # Instruments rect
    instrument_rects = []
    for i in range(instruments):
        rect = pg.rect.Rect((0, i * 100), (200, 100))
        instrument_rects.append(rect)
    if beat_changed:
        play_notes()
        beat_changed = False
    if save_menu:
        exit_button, saving_button, beat_name, entry_rect = draw_save_menu(
            beat_name, typing
        )
    elif load_menu:
        (
            exit_button,
            loading_button,
            entry_rect,
            delete_button,
            loaded_information,
        ) = draw_load_menu(index)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        if event.type == pg.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    coords = boxes[i][1]
                    clicked[coords[1]][coords[0]] *= -1
        if event.type == pg.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause_button.collidepoint(event.pos) and playing:
                playing = False
            elif play_pause_button.collidepoint(event.pos) and not playing:
                playing = True
                active_beat = 0
                active_length = 0
            if beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
            if bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            if clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
            for i in range(len(instrument_rects)):
                if instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
            if save_button.collidepoint(event.pos):
                save_menu = True
            if load_button.collidepoint(event.pos):
                load_menu = True
                playing = False
        elif event.type == pg.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                typing = False
                beat_name = ""
            if entry_rect.collidepoint(event.pos):
                if save_menu:
                    if typing:
                        typing = False
                    else:
                        typing = True
                if load_menu:
                    index = (event.pos[1] - 100) // 50
            if save_menu:
                if saving_button.collidepoint(event.pos):
                    file = open("saved_beats.txt", "w")
                    saved_beats.append(
                        f"\nname: {beat_name}, beats: {beats}, bpm: {bpm}, selected: {clicked}"
                    )
                    for i in range(len(saved_beats)):
                        file.write(str(saved_beats[i]))
                    file.close()
                    save_menu = False
                    load_menu = False
                    playing = True
                    typing = False
                    beat_name = ""
            if load_menu:
                if delete_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        saved_beats.pop(index)
                if loading_button.collidepoint(event.pos):
                    if 0 <= index < len(saved_beats):
                        beats = loaded_information[0]
                        bpm = loaded_information[1]
                        clicked = loaded_information[2]
                        index = 100
                        save_menu = False
                        load_menu = False
                        playing = True
                        typing = False
        if event.type == pg.TEXTINPUT and typing:
            beat_name += event.text
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE and len(beat_name) > 0:
                beat_name = beat_name[:-1]  # to remove the last character , one by one

    beat_length = 3600 // bpm  # Beat length in seconds

    if playing:
        if active_length < beat_length:
            active_length += 1
            beat_changed = True
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
            else:
                active_beat = 0
            beat_changed = True
    pg.display.flip()

file = open("saved_beats.txt", "w")
for i in range(len(saved_beats)):
    file.write(str(saved_beats[i]))
file.close()

pg.quit()
