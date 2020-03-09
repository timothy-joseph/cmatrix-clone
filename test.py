#!/bin/python3
import curses as nc
import time
import string
import random

stdscr = nc.initscr();
h, w = stdscr.getmaxyx();
w -= 1;
nc.curs_set(0);
nc.noecho();

# t_interval = 0.05 # seconds
t_int_low = 0.01 / w;
t_int_high = 0.1 / w;
chars = string.ascii_letters + string.digits + string.punctuation

sequences = [None] * w;

def get_rand_seq():
    '''
    get a random string of characters of lenght = h,
    then a random number 1 < l <= h which is the lenght
    of the sequence to be shown

    rtype: dict = { "l": l,
                    "seq": list of random non-blank chars of lenght h,
                    "start": the lowest char in the list,
                    "time": the time interval, doesn't really seem to affect it all that much, probably not worth even adding
                  }

    '''

    global h, chars;

    ret = {};

    ret["seq"] = random.sample(chars, h)
    ret["l"] = random.randint(2, h);
    ret["start"] = 0;
    ret["time"] = random.uniform(t_int_low, t_int_high);

    return ret;

def update_seq(i):
    global h, sequences;

    # check if blank
    if sequences[i] == None:
        if random.randint(1, 50) == 10:
            sequences[i] = get_rand_seq();

        return;
    
    # scroll down
    sequences[i]["start"] += 1;
    if sequences[i]["start"] - sequences[i]["l"] >= 0:
        stdscr.addch(sequences[i]["start"] - sequences[i]["l"], i, " ");

    if sequences[i]["start"] < h:
        if sequences[i]["start"] - sequences[i]["l"]+1 >= 0:
            stdscr.addch(sequences[i]["start"] - sequences[i]["l"]+1, i, sequences[i]["seq"][sequences[i]["start"] - sequences[i]["l"]], nc.A_DIM);
        stdscr.addch(sequences[i]["start"]-1, i, sequences[i]["seq"][sequences[i]["start"]], nc.A_DIM);
        stdscr.addch(sequences[i]["start"], i, sequences[i]["seq"][sequences[i]["start"]]);

    if sequences[i]["start"] == h:
        stdscr.addch(sequences[i]["start"]-1, i, sequences[i]["seq"][sequences[i]["start"]-1], nc.A_DIM);
    
    # check if we need to update sequences[i] = None
    if sequences[i]["start"] - sequences[i]["l"] >= h-1:
        sequences[i] = None;

while 1:
    for i in range(1, w):
        update_seq(i);
        stdscr.refresh();
        if (sequences[i]):
            time.sleep(sequences[i]["time"]);

nc.endwin();
