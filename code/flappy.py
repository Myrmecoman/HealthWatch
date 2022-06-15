from init import *
from var import *
import random

def generate_pipe():
    pipe = [1 for i in range(64)]

    top = random.randint(5, 40)
    for i in range(top, top + 20):
        pipe[i] = 0

    return pipe
    
def flappy():
    oled.fill(0)
    oled.show()

    TIMING = 4000
    clock = utime.ticks_ms() - TIMING 

    bird_pos = [63, 31]
    score = 0

    while True:
        oled.pixel(bird_pos[0], bird_pos[1], 0)
        oled.scroll(-1, 0)

        if getVrY() != 0:
            bird_pos[1] -= 5
        else:
            bird_pos[1] += 2

        if oled.pixel(bird_pos[0], bird_pos[1]) or bird_pos[1] < 0 or bird_pos[1] >= 64:
            break

        score += int(oled.pixel(bird_pos[0] - 1, 0) and not oled.pixel(bird_pos[0], 0))
        
        oled.pixel(bird_pos[0], bird_pos[1], 1)

        if utime.ticks_ms() - clock >= TIMING:
            pipe = generate_pipe()

            for i in range(len(pipe)):
                oled.pixel(124, i, pipe[i])
                oled.pixel(125, i, pipe[i])
                oled.pixel(126, i, pipe[i])
            
            clock = utime.ticks_ms()
        
        oled.show()

    write(10, 10, "Score: " + str(score), CC, 108, 44, 1, 2)
    oled.show()

    swap = 0
    while True:
        swap = (getBMid(), swap)[swap != 0]
        if swap != 0 and getBMid() == 0:
            return swap