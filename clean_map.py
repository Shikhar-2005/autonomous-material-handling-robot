from PIL import Image
import numpy as np

img = Image.open('/home/shikh/my_map_v3.pgm').convert('L')
arr = np.array(img)

# Only clean grey pixels INSIDE the map (value 205-211 specifically)
arr[(arr >= 205) & (arr <= 211)] = 254

cleaned = Image.fromarray(arr)
cleaned.save('/home/shikh/my_map_v3.pgm')
print("Done")
