# deep_learning_othello  

## Toy example on MNIST  
We trained MNIST using simple MLP and CNN. MLP can get 95% accuracy and CNN can get 98%.  

It seems that when doing small datasets like MNIST, the training time is quite short. Thus, although the training speed of GPU is much quicker than CPU, the overhead of loading data into GPU is quite disappointing.  

According to the official guide, they think that if we are working on a real dataset, which means that the datasets get much larger and the models are much more complex, the overhead time compared to training time is negligible.  

As we still do not know how complex our model will be, GPU is not so important at this time.  
