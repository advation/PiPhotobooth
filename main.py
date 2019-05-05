import os
import sys
import time
import uuid
import pygame
import pygame.camera
from pygame import mouse
from pygame.locals import *

pygame.init()
(width, height) = (800, 500)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

pygame.display.set_caption('Photo Booth')

pygame.camera.init()
cameras = pygame.camera.list_cameras()

cam = pygame.camera.Camera(cameras[0], (640, 480))
cam.start()
cam.set_controls(vflip=True, hflip=False)

pygame.mouse.set_visible(False)

print_image = False
print_amount = 1
print_wait_time = 65000  # 1000 = 1 second

BLACK = (0, 0, 0)
DARK_GREY = (55, 62, 72)
WHITE = (242, 242, 242)
RED = (200, 55, 55)
BLUE = (55, 113, 200)
GREEN = (44, 160, 90)

captured_image = None


# Check for root
def root_check():
    if os.getuid() != 0:
        print('This must be run as root')
        sys.exit(1)


def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()


# Display message
def message_display(text):
    largeText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 50)
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((width / 2), (height / 2))
    screen.blit(TextSurface, TextRect)


# Display message along the top
def message_display_top(text):
    largeText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((width / 2), 30)
    screen.blit(TextSurface, TextRect)


# Display message center
def message_display_large(text):
    largeText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 50)
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((width/2), (height/2))
    screen.fill(BLACK)
    screen.blit(TextSurface, TextRect)


# Display message center
def message_display_xlarge(text):
    largeText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 120)
    TextSurface, TextRect = text_objects(text, largeText)
    TextRect.center = ((width/2), (height/2))
    screen.blit(TextSurface, TextRect)


def display_retake():
    normalText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects("Retake", normalText)
    screen.blit(TextSurface, (45, (height/2)+110))


def display_print():
    normalText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects("Print", normalText)
    screen.blit(TextSurface, (670, (height/2)+110))


def one_print():
    normalText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects("1 Copy", normalText)
    screen.blit(TextSurface, (150, (height/2)+110))


def two_print():
    normalText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects("2 Copies", normalText)
    screen.blit(TextSurface, (340, (height/2)+110))


def three_print():
    normalText = pygame.font.Font('/home/pi/PiPhotobooth/Ubuntu-R.ttf', 30)
    TextSurface, TextRect = text_objects("3 Copies", normalText)
    screen.blit(TextSurface, (540, (height / 2) + 110))


def clear_screen():
    screen.fill(BLACK)


def capture_image():
    global cam
    uid = time.strftime("%Y-%m-%d_%H%M%S")
    image = cam.get_image()
    pygame.image.save(image, '/home/pi/PiPhotobooth/images/%s.jpg' % uid)
    return uid


def send_to_printer(uid):
    print("Printing image...")
    os.system("lp -d Canon_SELPHY_CP1300 /home/pi/PiPhotobooth/images/%s.jpg" % uid)


def clear_print_queue():
    print("Clearing print queue...")
    os.system("cancel -a Canon_SELPHY_CP1300")


# Main Program Loop
def main_loop():

    global cam
    run = True
    clear_screen()
    pygame.mouse.set_visible(False)

    while run:
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                print("Exiting...")
                sys.exit(1)

            # Exit event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting...")
                    sys.exit(1)

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        image = cam.get_image()
        screen.blit(image, (80, 15))
        message_display("Tap here to take a picture")

        pygame.display.update()


def capture_loop():
    global captured_image, cam
    clear_screen()
    start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    #message_display("Printing picture...")

    while current_time < start_time + 6000:
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                print("Exiting...")
                sys.exit(1)

            # Exit event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting...")
                    sys.exit(1)

        image = cam.get_image()
        if current_time > start_time < (start_time + 999):

            screen.blit(image, (80, 15))
            message_display_xlarge("5")

        if current_time > (start_time + 1000) < (start_time + 1999):

            screen.blit(image, (80, 15))
            message_display_xlarge("4")

        if current_time > (start_time + 2000) < (start_time + 2999):

            screen.blit(image, (80, 15))
            message_display_xlarge("3")

        if current_time > (start_time + 3000) < (start_time + 3999):

            screen.blit(image, (80, 15))
            message_display_xlarge("2")

        if current_time > (start_time + 4000) < (start_time + 4999):

            screen.blit(image, (80, 15))
            message_display_xlarge("1")

        if current_time > start_time + 5000:
            screen.blit(image, (80, 15))
            message_display_xlarge("")
            cam.stop()
            cam.start()
            captured_image = capture_image()

        pygame.display.update()
        current_time = pygame.time.get_ticks()


def review_loop():
    global print_image, captured_image
    clear_screen()
    start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    pygame.mouse.set_visible(True)

    run = True
    while run:
        for event in pygame.event.get():
            # Exit event
            if event.type == pygame.QUIT:
                print("Exiting...")
                sys.exit(1)

            # Exit event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Exiting...")
                    sys.exit(1)

            # Mouse Button Down Event
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_position = pygame.mouse.get_pos()

                if 0 < mouse_position[0] < 400 and height > mouse_position[1] > 0:
                    print_image = False
                    run = False

                if 401 < mouse_position[0] < 800 and height > mouse_position[1] > 0:
                    print_image = True
                    run = False

        if current_time > start_time + 30000:
            print_image = False
            break

        if run is False:
            break

        current_time = pygame.time.get_ticks()

        image = pygame.image.load('/home/pi/PiPhotobooth/images/%s.jpg' % captured_image)
        screen.blit(image, (80, 15))
        pygame.draw.rect(screen, RED, [20, ((height/2)+50), 150, 150])
        pygame.draw.rect(screen, GREEN, [630, ((height/2)+50), 150, 150])
        display_retake()
        display_print()
        pygame.display.update()


def print_amount_loop():
    global print_image, captured_image, print_amount
    start_time = pygame.time.get_ticks()
    current_time = pygame.time.get_ticks()
    clear_screen()
    pygame.mouse.set_visible(True)

    if print_image is True:
        run = True
        while run:
            for event in pygame.event.get():
                # Exit event
                if event.type == pygame.QUIT:
                    print("Exiting...")
                    sys.exit(1)

                # Exit event
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("Exiting...")
                        sys.exit(1)

                # Mouse Button Down Event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_position = pygame.mouse.get_pos()

                    if 0 < mouse_position[0] < 299 and height > mouse_position[1] > 0:
                        print_image = True
                        run = False

                    if 300 < mouse_position[0] < 499 and height > mouse_position[1] > 0:
                        print_image = True
                        print_amount = 2
                        run = False

                    if 500 < mouse_position[0] < 800 and height > mouse_position[1] > 0:
                        print_image = True
                        print_amount = 3
                        run = False

            if current_time > start_time + 30000:
                break

            if run is False:
                break

            current_time = pygame.time.get_ticks()

            image = pygame.image.load('/home/pi/PiPhotobooth/images/%s.jpg' % captured_image)
            screen.blit(image, (80, 15))

            message_display("How many copies?")

            pygame.draw.rect(screen, BLUE, [125, ((height / 2) + 50), 150, 150])
            one_print()

            pygame.draw.rect(screen, BLUE, [325, ((height / 2) + 50), 150, 150])
            two_print()

            pygame.draw.rect(screen, BLUE, [525, ((height / 2) + 50), 150, 150])
            three_print()

            pygame.display.update()


def print_loop():
    global print_image, captured_image, print_amount
    clear_screen()
    pygame.mouse.set_visible(False)
    if print_image is True:

        message_display("Printing picture...")
        print("Send print to printer")
        pygame.display.update()

        send_to_printer(captured_image)
        time.sleep(68)

        if print_amount >= 2:
            send_to_printer(captured_image)
            time.sleep(68)

        if print_amount == 3:
            send_to_printer(captured_image)
            time.sleep(68)

    else:
        print("Print rejected")

    print_image = False
    captured_image = None


if __name__ == "__main__":

    # Clear print queue
    clear_print_queue()

    # Start main program loop
    while True:
        main_loop()
        clear_screen()

        capture_loop()
        clear_screen()

        review_loop()
        clear_screen()

        print_amount_loop()
        clear_screen()

        print_loop()
        clear_screen()