import tensorflow as tf
import numpy as np
import os
import time
import datetime
from getData import data_helpers
from getData import categories
from learning import text_cnn
from tensorflow.contrib import learn

import csv
import json

def evaluate(data):
    dir = os.path.dirname(os.path.realpath(__file__))
    dir += "/runs/1503432797/checkpoints"

    # Taken from https://github.com/dennybritz/cnn-text-classification-tf/blob/master/eval.py

    # Data parameters

    # for cat in categories.categories100:
        # tf.flags.DEFINE_string(cat,"./getData/data/100/"+cat+".txt", "Titles taken from /r/" + cat + "/")
    '''
    tf.flags.DEFINE_string("input","input","input")

    # Eval parameters
    tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
    tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
    tf.flags.DEFINE_boolean("eval_train",True, "Evaluate on all training data")

# Misc Parameters
    tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
    tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

    
    FLAGS = tf.flags.FLAGS
    FLAGS._parse_flags()
    print("\nParameters:")
    for attr, value in sorted(FLAGS.__flags.items()):
        print("{}={}".format(attr.upper(), value))
    print("")
    '''

    # CHANGE THIS: Load data. Load your own data here
    if True:
        x_raw = data_helpers.load_data_from_array(data)
        # y_test = np.argmax(y_test, axis=1)
        y_test = None
    else:
        x_raw = ["a masterpiece four years in the making", "everything is off."]
        y_test = [1, 0]

    # Map data into vocabulary
    vocab_path = os.path.join(dir, "..", "vocab")
    vocab_processor = learn.preprocessing.VocabularyProcessor.restore(vocab_path)
    x_test = np.array(list(vocab_processor.transform(x_raw)))

    print("\nEvaluating...\n")

    # Evaluation
    # ==================================================
    checkpoint_file = "/home/ubuntu/ml-eval-server/learning/runs/1503432797/checkpoints/model-54700"
    print(checkpoint_file)
    graph = tf.Graph()
    with graph.as_default():
        session_conf = tf.ConfigProto(
          allow_soft_placement=True,
          log_device_placement=False)
        sess = tf.Session(config=session_conf)
        with sess.as_default():
            # Load the saved meta graph and restore variables
            saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
            saver.restore(sess, checkpoint_file)

            # Get the placeholders from the graph by name
            input_x = graph.get_operation_by_name("input_x").outputs[0]
            # input_y = graph.get_operation_by_name("input_y").outputs[0]
            dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

            # Tensors we want to evaluate
            predictions = graph.get_operation_by_name("output/predictions").outputs[0]

            # Generate batches for one epoch
            batches = data_helpers.batch_iter(list(x_test), 64, 1, shuffle=False)

            # Collect the predictions here
            all_predictions = []

            for x_test_batch in batches:
                batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
                all_predictions = np.concatenate([all_predictions, batch_predictions])

    # Print accuracy if y_test is defined
    if y_test is not None:
        correct_predictions = float(sum(all_predictions == y_test))
        print("Total number of test examples: {}".format(len(y_test)))
        print("Accuracy: {:g}".format(correct_predictions/float(len(y_test))))

    # Save the evaluation to a csv
    predictions_human_readable = np.column_stack((np.array(x_raw), all_predictions))
    results = predictions_human_readable.tolist()

    out = dict()
    out['data'] = dict()
    for x in range(0,len(results)):
        out['data'][x] = dict()
        out['data'][x]['query'] = results[x][0]
        out['data'][x]['value'] = results[x][1]
    web = json.loads(json.dumps(out))

    dts = datetime.datetime.utcnow()
    curtime = int(time.mktime(dts.timetuple()) + dts.microsecond/1e6)
    '''
    out_path = os.path.join(dir, "..", str(curtime) + "_prediction.csv")
    print("Saving evaluation to {0}".format(out_path))
    with open(out_path, 'w') as f:
        csv.writer(f).writerows(predictions_human_readable)
    '''

    return web