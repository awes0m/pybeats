from pickle import FALSE
import pygame as pg
from pygame import MOUSEBUTTONUP, mixer

# initialize pg
pg.init()


WIDTH = 1366
HEIGHT = 710

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
gray = (128, 128, 128)
green = (0, 255, 0)
gold = (212, 175, 55)
blue = (0, 255, 255)
dark_gray = (64, 64, 64)


screen = pg.display.set_mode([WIDTH, HEIGHT])
pg.display.set_caption("Py Beats")
label_font = pg.font.SysFont("Ariel", 35)
medium_font = pg.font.SysFont("Ariel", 25)
# label_font = pg.font.SysFont( "assets/Roboto-Bold.ttf", 3050, bold=pg.font.Font.bold)

fps = 60
timer = pg.time.Clock()
beats = 8
instruments = 6
boxes = []
clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]
active_list = [1 for _ in range(instruments)]
bpm = 240
playing = True
active_length = 0
active_beat = 1
beat_changed = True
save_menu = False
load_menu = False
saved_beats=[]
file = open("saved_beats.txt", "r")
# for line in file:
#     saved_beats.append(line)
saved_beats.extend(iter(file))

beat_name = ''
typing = False



# load in sounds
hi_hat = mixer.Sound("./assets/sounds/hi hat.wav")
snare = mixer.Sound("./assets/sounds/snare.wav")
kick = mixer.Sound("./assets/sounds/kick.wav")
crash = mixer.Sound("./assets/sounds/crash.wav")
clap = mixer.Sound("./assets/sounds/clap.wav")
tom = mixer.Sound("./assets/sounds/tom.WAV")
pg.mixer.set_num_channels(instruments * 4)


def play_notes():
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


def draw_grid(clicks, beat, actives):
    # left_box = pg.draw.rect(screen,white , [0, 0, 200, HEIGHT])
    left_box_outline = pg.draw.rect(screen, gray, [0, 0, 200, HEIGHT], 5)
    bottom_panel = pg.draw.rect(screen, black, [0, HEIGHT - 120, WIDTH, 120])
    bottom_panel_outline = pg.draw.rect(
        screen, gray, [0, HEIGHT - 120, WIDTH, 120], 12
    )

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
    for i in range(instruments):
        pg.draw.line(screen, gray, (0, (i * 100) + 100), (200, (i * 100) + 100), 3)

    for i in range(beats):
        for j in range(instruments):
            color = (
                gray if clicks[j][i] == -1 else green if actives[j] == 1 else dark_gray
            )
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
                instruments * 100,
            ],
            5,
            3,
        )
    return boxes


 ## SCREENS ##
def draw_save_menu(beat_name,typing,):
    pg.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    menu_text = label_font.render("Save Menu:  Enter a Name for Current Beats", True, white)
    screen.blit(menu_text, (WIDTH // 2 - 300, HEIGHT // 2 - 300))
    saving_btn = pg.draw.rect(screen, dark_gray, [WIDTH // 2 - 200, HEIGHT *0.75, 400, 100],0,5)
    saving_text = label_font.render("Save Beat", True, white)
    screen.blit(saving_text, (WIDTH // 2 - 50, HEIGHT *0.75 +40))
    exit_btn = pg.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90],0,5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 150, HEIGHT - 65 ))
    entry_rect = pg.draw.rect(screen,gray, [400, 200, 600, 200],5,5)
    entry_text = label_font.render(f'{beat_name}', True, white)
    screen.blit(entry_text,(430,250))
    return exit_btn ,saving_btn,entry_rect

def draw_load_menu():
    pg.draw.rect(screen, black, [0, 0, WIDTH, HEIGHT])
    exit_btn = pg.draw.rect(screen, gray, [WIDTH - 200, HEIGHT - 100, 180, 90],0,5)
    exit_text = label_font.render("Close", True, white)
    screen.blit(exit_text, (WIDTH - 150, HEIGHT - 65 ))
    return exit_btn


run = True
while run:
    timer.tick(fps)
    screen.fill(black)
    
    boxes = draw_grid(clicked, active_beat, active_list)

    # lower menu buttons
    play_pause_button = pg.draw.rect(
        screen, gray, [50, HEIGHT - 100, 100, 80], 0, 5
    )
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

    # Instruments rect
    Instrument_rects = []
    for i in range(instruments):
        rect = pg.rect.Rect((0, i * 100), (200, 100))
        Instrument_rects.append(rect)

    # save and load stuff

    save_button = pg.draw.rect(screen, gray, [700, HEIGHT - 100, 200, 37], 0, 5)
    save_text = label_font.render("Save Beat", True, white)
    screen.blit(save_text, (720, HEIGHT - 90))
    load_button = pg.draw.rect(screen, gray, [700, HEIGHT - 60, 200, 37], 0, 5)
    load_text = label_font.render("Load Beat", True, white)
    screen.blit(load_text, (720, HEIGHT - 50))

    # clear_board
    clear_button = pg.draw.rect(screen, gray, [950, HEIGHT - 80, 200, 40], 0, 5)
    clear_text = label_font.render("Clear Board", True, black)
    screen.blit(clear_text, (970, HEIGHT - 70))
    
    if save_menu:
        exit_button, saving_btn , entry_rectangle =draw_save_menu(beat_name, typing)
    if load_menu:
        exit_button = draw_load_menu()

    if beat_changed:
        play_notes()
        beat_changed = False

    for event in pg.event.get():
        # Close window
        if event.type == pg.QUIT:
            run = False
        # Mouse click   
        if event.type == pg.MOUSEBUTTONDOWN and not save_menu and not load_menu:
            for i in range(len(boxes)):
                if boxes[i][0].collidepoint(event.pos):
                    cords = boxes[i][1]
                    clicked[cords[1]][cords[0]] *= -1
        
        if event.type == pg.MOUSEBUTTONUP and not save_menu and not load_menu:
            if play_pause_button.collidepoint(event.pos):
                playing = not playing
            elif bpm_add_rect.collidepoint(event.pos):
                bpm += 5
            elif bpm_sub_rect.collidepoint(event.pos):
                bpm -= 5
            elif beats_add_rect.collidepoint(event.pos):
                beats += 1
                for i in range(len(clicked)):
                    clicked[i].append(-1)
            elif clear_button.collidepoint(event.pos):
                clicked = [[-1 for _ in range(beats)] for _ in range(instruments)]

            elif beats_sub_rect.collidepoint(event.pos):
                beats -= 1
                for i in range(len(clicked)):
                    clicked[i].pop(-1)
                    
            elif save_button.collidepoint(event.pos):
                save_menu = True
            elif load_button.collidepoint(event.pos):
                load_menu = True

            for i in range(len(Instrument_rects)):
                if Instrument_rects[i].collidepoint(event.pos):
                    active_list[i] *= -1
                    
                    
        elif event.type == pg.MOUSEBUTTONUP:
            if exit_button.collidepoint(event.pos):
                save_menu = False
                load_menu = False
                playing = True
                beat_name =''
                typing = False
            if entry_rectangle.collidepoint(event.pos):
                if typing:
                    typing = False
                elif not typing:
                    typing = True
            if event.type ==pg.TEXTINPUT and typing:
                beat_name += event.text
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE and len(beat_name)>0 and typing:
                    beat_name = beat_name[:-1]        
                
                    
    beat_length = 3600 // bpm  # Beat length in seconds

    if playing:
        if active_length < beat_length:
            active_length += 1
        else:
            active_length = 0
            if active_beat < beats - 1:
                active_beat += 1
            else:
                active_beat = 0
            beat_changed = True
    pg.display.flip()


pg.quit()
