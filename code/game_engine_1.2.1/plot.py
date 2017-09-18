import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

# f = file("cat_train_set_L_NEW.npy", "rb")
# data = np.load(f)
# label = np.load(f)

# # print label.shape
# distribution = pd.value_counts(label, sort=False)
# x = np.arange(17)-8
# plt.bar(x, distribution[x])
# plt.xlabel('Score label')
# plt.ylabel('Frequency')
# plt.title('Score Distribution')
# plt.xticks(x, x)

train_scores = [0.0788, 0.1925, 0.2142, 0.2319, 0.2490, 0.2714, 0.2995, 0.3346, 0.3743, 0.4196, 0.4704, 0.5218, 0.5736, 0.6291, 0.6843, 0.7297, 0.7678, 0.8022, 0.8617, 0.9004, 0.8827]

val_scores = [0.0802, 0.1937, 0.2120, 0.2235, 0.2373, 0.2437, 0.2559, 0.2621, 0.2673, 0.2683, 0.2666, 0.2670, 0.2641, 0.2664, 0.2603, 0.2556, 0.2520, 0.2519, 0.2474, 0.2433, 0.2414]

plt.plot(range(21), train_scores,
         color='blue', marker='o',
         markersize=5, label='training accuracy')

plt.plot(range(21), val_scores,
         color='green', linestyle='--',
         marker='s', markersize=5,
         label='validation accuracy')

plt.grid()
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.legend(loc='lower right')
plt.ylim([0.0, 1.0])
plt.tight_layout()
# # plt.savefig(time.strftime('./figures/CNN_cat_tuning_epoch_learning_curve_%Y%m%d%H%M.png'), dpi=300)
plt.show()
