"""
Interface to the neural translation model.
"""
import tensorflow as tf

import os
import sys

learning_module_dir = os.path.join(os.path.dirname(__file__), "..",
                                   "tellina_learning_module")
sys.path.append(learning_module_dir)

from encoder_decoder import classifiers
from encoder_decoder import data_utils
from encoder_decoder import decode_tools
from encoder_decoder import translate as trans

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

FLAGS = tf.app.flags.FLAGS

FLAGS.demo = True
FLAGS.fill_argument_slots = True
FLAGS.num_nn_slot_filling = 5

FLAGS.normalized = True
FLAGS.encoder_topology = 'birnn'

FLAGS.sc_token_dim = 150
FLAGS.batch_size = 128
FLAGS.num_layers = 1
FLAGS.learning_rate = 0.0001
FLAGS.sc_input_keep = 0.6
FLAGS.sc_output_keep = 0.6
FLAGS.tg_input_keep = 0.6
FLAGS.tg_output_keep = 0.6

FLAGS.tg_token_use_attention = True
FLAGS.tg_token_attn_fun = 'non-linear'
FLAGS.attention_input_keep = 0.6
FLAGS.attention_output_keep = 0.6
FLAGS.beta = 0.0

FLAGS.decoding_algorithm = 'beam_search'
FLAGS.beam_size = 100
FLAGS.alpha = 1.0

FLAGS.nl_vocab_size = 3100
FLAGS.cm_vocab_size = 3400
FLAGS.sc_token_embedding_size = 630
FLAGS.sc_vocab_size = 3100
FLAGS.tg_token_embedding_size = 400
FLAGS.tg_vocab_size = 3400

FLAGS.dataset = 'bash'
FLAGS.data_dir = os.path.join(learning_module_dir, "data", FLAGS.dataset)
FLAGS.model_root_dir = os.path.join(learning_module_dir, "model", "seq2seq")

# create tensorflow session
sess = tf.Session(config=tf.ConfigProto(allow_soft_placement=True,
                  log_device_placement=FLAGS.log_device_placement))

# create model and load nerual model parameters.
model = trans.create_model(sess, forward_only=True, buckets=[(30, 40)])
vocabs = data_utils.load_vocab(FLAGS)

if FLAGS.fill_argument_slots:
    # create slot filling classifier
    model_param_dir = os.path.join(FLAGS.model_dir, 'train.mappings.X.Y.npz')
    train_X, train_Y = data_utils.load_slot_filling_data(model_param_dir)
    slot_filling_classifier = classifiers.KNearestNeighborModel(
        FLAGS.num_nn_slot_filling, train_X, train_Y)
    print('Slot filling classifier parameters loaded.')
else:
    slot_filling_classifier = None

def translate_fun(sentence, slot_filling_classifier=slot_filling_classifier):
    print('start running translation model')
    print(sentence)
    return decode_tools.translate_fun(sentence, sess, model, vocabs, FLAGS,
                                      slot_filling_classifier)
