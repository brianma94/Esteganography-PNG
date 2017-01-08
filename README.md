# Esteganography-PNG
Esteganography script in images PNG

This project was done by a classmate Pau Peña and me, Brian Martinez Alvarez.
It is a Python script that permits to encode or decode a message into PNG images. Doesn't matter if it uses RGB or RGBA to set the pixels. It works in both. 
It uses the LSB-Algorythm.

It is necessary the following libraries to execute the script:

- Image from PIL
- sys
- os

<b><h2>IMPORTANT!!!</h2></b>
- The message needs to contain only ASCII characters
- The message is not encrypted, it is inserted on the pixels in plain text.

To execute it is just necessary this steps:

<b><h3>To see the options:</h3></b>

    python esteganography.py --h


<b><h3>To encode:</h3></b>

    python esteganography.py --encode original_image.png modified_image.png 'Hello World'

Where 'original_image.png' is the image that you choose to encode the message, 'modified_image.png' is the same image as the original but with the message encoded and 'Hello World' will be the hidden message.
It will create the 'modified_image.png' in the same directory and it will be identical to the original image.

<b><h3>To  decode:</h3></b>

    python esteganography.py --decode modified_image.png"

Where modified_image.png is the image where you want to decode the hidden message. If the image does't have any message, it won't prompt anything. Otherwise, it will prompt the hidden message in the terminal.

