from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


def striped_image(size):
    pels = np.ndarray((size[1], size[0], 3), dtype=np.int8)
    height = size[1]
    quarter_w = size[0]/4
    # 4 columns of different colour.
    for i in range(height):
        pels[i, 0:quarter_w, 0] = 255  # 1st column red
        pels[i, quarter_w:quarter_w*2, 1] = 255  # 2nd column green
        pels[i, quarter_w*2:quarter_w*3, 2] = 255  # 3rd column blue
    img = Image.frombuffer("RGB", size, pels, 'raw', "RGB", 0, 1)
    return img


plt.imshow(striped_image((256,256))); plt.show()
plt.imshow(striped_image((256,256))); plt.show()
plt.imshow(striped_image((256,256))); plt.show()
plt.imshow(striped_image((256,256))); plt.show()


plt.subplot(2,2,1); plt.imshow(striped_image((256,256)))
plt.subplot(2,2,2); plt.imshow(striped_image((256,256)))
plt.subplot(2,2,3); plt.imshow(striped_image((256,256)))
plt.subplot(2,2,4); plt.imshow(striped_image((256,256)))
plt.show()

