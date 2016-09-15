##Usage  

Put the photos you want to predict in to the directory '/photos', then run the 'vgg_16_predict.py'. The predicted images will be in the folder '/predict' with the name of predicted genre.  

###Caution  

If you are using GPU, be sure that your GPU has enough memory...... Mine is not sufficient to load the huge model of VGG16. Anyway, we donot need to train model here, just use it wo classify. CPU is enough for the task.  

If you encounter errors like "you might consider using 'theano.shared(..., borrow=True)", just change you theano settings from gpu to cpu.
