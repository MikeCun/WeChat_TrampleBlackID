import numpy as np
import os, cv2, wda

# Screen Size for the Phone
screen_w, screen_h = 1242, 2208
black_w, black_h = 310, 384

# IOS WDA Client
SeverURL = "http://localhost:8100"
client = wda.Client(SeverURL)
s = client.session()

while True:
    # IOS SreenShot
    client.screenshot('block.png')
    if not os.path.exists('block.png'):
        raise NameError('Cannot obtain screenshot from the phone!')

    # Read the last line
    block = cv2.imread('block.png')
    dentifier = block[-black_h:screen_h, 0:screen_w, :]
    Min = np.array([1.0, 2.0, 3.0, 4.0])

    # Sum the RGB in the cube and select the Min one
    for i in range(4):
        Min[i] = dentifier[:, i * black_w:black_w * (i + 1), :].sum()
    s.tap((black_w / 2 + Min.argmin() * black_w) / 3, (screen_h - black_h / 2) / 3)
