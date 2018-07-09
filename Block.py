import numpy as np
import time
import os
import cv2
import wda
client = wda.Client(severURL)
s = client.session()
black = np.zeros((504, 310, 3))
while True:
    client.screenshot('block.png')
    if not os.path.exists('block.png'):
        raise NameError('Cannot obtain screenshot from the phone!')
    block = cv2.imread('block.png')
    dentifier = block[1704:2208, 0:1242]
    for i in range(4):
        if dentifier[:, i*310:310*(i+1)].all() == black.all():
            s.tap(1956, i*310+155)
            print i
    time.sleep(5)
