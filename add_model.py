
import pickle
from fakenews_model import train_model

with open("fakenews_model.bin", 'wb') as f_out:
    pickle.dump(train_model(), f_out)
    f_out.close()
