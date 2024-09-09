from PIL import Image
import numpy as np

def encode_message(image_path, message, output_image_path):
    # Open the original image
    img = Image.open(image_path)
    img = img.convert('RGB')
    pixels = np.array(img) #Conversion of 'RGB' image into a 2-D array

    # Convert the message to binary
    #'ord' is used to convert the message into integer and 'format' is used for conversion of those integers into 8 bits (0-padded)  
    binary_message = ''.join(format(ord(char), '08b') for char in message) + '00000000'  # Add a delimiter (null character)

    # Check if the message fits in the image
    max_message_length = pixels.size // 8
    if len(binary_message) > max_message_length:
        raise ValueError("Message is too long to fit in the image")

    # Flatten the pixels array and encode the message
    flat_pixels = pixels.flatten()
    #Encoading of message as bits in the pixels
    for i in range(len(binary_message)):
        flat_pixels[i] = (flat_pixels[i] & ~1) | int(binary_message[i]) #Removal of LSB(Least Significant Bit and replacing it with message bit)
    
    # Reshape back to the original shape and save the image
    encoded_pixels = flat_pixels.reshape(pixels.shape)
    encoded_img = Image.fromarray(encoded_pixels.astype(np.uint8))
    encoded_img.save(output_image_path)

    print("Encoding complete")