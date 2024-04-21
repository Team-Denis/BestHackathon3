from matplotlib.image import imread
import numpy as np
from PIL import Image

# change working directory
import os
# os.chdir("ant_code/image_obsfucation")

# In[2]:
image = imread('data/img_V2.png')[:, :, 0:3]


# convert image to 8 bit per channel
image = (image * 255).astype(np.uint8)

with open('output/encoded_image.BMP', 'wb') as f:
    # encode BMP image
    Image.fromarray(image).save(f, 'BMP')

code_encode = r"Un des 2 fragment eau 5739 BTW j'adore le 50Hz wink wink"
# convert code to binary string forcing it to be 8 bits long
caracters_values = [ord(c) for c in code_encode]
for value in caracters_values:
    assert value < 256
code_string = ''.join([format(c, '08b') for c in caracters_values])
print(code_string)
code_string

# In[8]:


encoding_length = image.shape[0] * image.shape[1] * image.shape[2]
print("encoding space 3 channels ", encoding_length)
print("encoding space 1 channel ", encoding_length // image.shape[2])
print("code length ", len(code_string))
assert len(code_string) <= encoding_length // image.shape[2]


# In[9]:


def encode_bit(bit, pixel_value):
    if bit == 1:
        if pixel_value % 2 == 0:
            return pixel_value + 1
        else:
            return pixel_value
    else:
        if pixel_value % 2 == 0:
            return pixel_value
        elif pixel_value == 0:
            return pixel_value + 1
        elif pixel_value == 255:
            return pixel_value - 1
        else:
            return pixel_value - 1



# In[11]:

for i in range(image.shape[0]):
    for j in range(image.shape[1]):
        if i * image.shape[1] + j < len(code_string):
            for k in range(image.shape[2]):
                image[i, j, k] = encode_bit(int(code_string[i * image.shape[1] + j]), image[i, j, k])
        else:
            for k in range(image.shape[2]):
                image[i, j, k] = encode_bit(0, image[i, j, k])

with open('output/encoded_image.bmp', 'wb') as f:
    # encode BMP image
    Image.fromarray(image).save(f, 'BMP')


# In[12]:


import re
def decode_bit(pixel_value):
    return pixel_value % 2


def decode_image(image):
    k = 0
    code_string = ''
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            code_string += str(decode_bit(image[i, j, k]))
    return code_string

def to_string(decoded_bits):
    caracters_values = [decoded_bits[i:i + 8] for i in range(0, len(decoded_bits), 8)]
    return ''.join([chr(int(c, 2)) for c in caracters_values])
    


# In[13]:


decoded_bits = decode_image(image)
decoded_string = to_string(decoded_bits)
decoded_string.strip("\x00"), len(decoded_string)


# In[14]:


code_string


# In[15]:


loaded_image = imread('output/encoded_image.bmp')
loaded_image.shape


# In[16]:


decoded_bits = decode_image(image)
decoded_string = to_string(decoded_bits)
print(decoded_string.strip("\x00"), len(decoded_string))


# In[ ]:




