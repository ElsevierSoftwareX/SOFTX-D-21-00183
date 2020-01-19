from skopt import gp_minimize
from skopt.callbacks import CheckpointSaver
from skopt.space import Integer, Real
from skopt.utils import use_named_args

from dataset.cifar_dataset import cifar_data
from neural_network import neural_network
from tensorflow.keras import backend as K

search_space = [
    Integer(16, 64, name='unit_c1'),
    Real(0.002, 0.3, name='dr1_2'),
    Integer(64, 128, name='unit_c2'),
    Integer(256, 512, name='unit_d'),
    Real(0.03, 0.5, name='dr_f'),
    Real(10 ** -5, 10 ** -1, name='learning_rate'),
    Integer(16, 128, name='batch_size')
]


# objective function
@use_named_args(search_space)
def objective(**params):
    f = open("hyperparameters_skopt.txt", "a")
    f.write(str(params) + "\n")
    n = neural_network(X_train, Y_train, X_test, Y_test, n_classes)
    score, history, model = n.training(params, False)
    f.close()
    K.clear_session()
    return -score[1]


X_train, X_test, Y_train, Y_test, n_classes = cifar_data()
checkpoint_saver = CheckpointSaver("checkpoints/checkpoint.pkl", compress=9)

# optimization
search_res = gp_minimize(objective, search_space, acq_func='EI', n_calls=20, n_random_starts=1,
                         callback=[checkpoint_saver])

print(search_res)
