from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import os

model = VGG16(weights='imagenet', include_top=True)

f = open('synset_words.txt','r')
lines = f.readlines()
f.close()

if __name__=='__main__':
    imgs = os.listdir("./photos")
    num = len(imgs)
    for i in range(num):
        img = image.load_img("./photos/"+imgs[i], target_size=(224, 224))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)
        features = model.predict(x)
        pre = np.argmax(features)
        save_image = image.load_img("./photos/"+imgs[i])
        save_image.save("./predict/"+lines[pre][10:]+".jpg")
        