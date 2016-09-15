# deep_learning_othello  

## Toy example on MNIST  
We trained MNIST using simple MLP and CNN. MLP can get 95% accuracy and CNN can get 98%.  

It seems that when doing small datasets like MNIST, the training time is quite short. Thus, although the training speed of GPU is much quicker than CPU, the overhead of loading data into GPU is quite disappointing.  

According to the official guide, they think that if we are working on a real dataset, which means that the datasets get much larger and the models are much more complex, the overhead time compared to training time is negligible.  

As we still do not know how complex our model will be, GPU is not so important at this time.  

## Application of VGG16  

By importing Keras application module, we can esaily use VGG16, VGG19 and other several famous models without training. The performance of VGG16 is really powerful and amazing! It can recognize cat, car, house and beach. More surprisingly, when we fed in the photos of apple and dog, it gave the answer "Granny Smith" (a tip-bearing apple cultivar) and "English foxhound" (one of the four foxhound breeds of dog). Even ourselves cannot recognize the specific species of the apple and dog!

Overall, the VGG16 is rather strong. We can set a webpage for people to upload photos and classify them online, and they well definitely be impressed of the power of deep learning.
