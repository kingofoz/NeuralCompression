'''
Created on Apr 18, 2015

@author: songhan
'''

import sys
import os
import numpy as np
import matplotlib.pyplot as plt


os.system("cd $CAFFE_ROOT")
caffe_root = os.environ["CAFFE_ROOT"]
print caffe_root
sys.path.insert(0, caffe_root + 'python')
import caffe

def analyze_param(net, layers):
#   plt.figure()
    print '\n=============analyze_param start==============='
    total_nonzero = 0
    total_allparam = 0
    percentage_list = []
    for i, layer in enumerate(layers):
        i += 1
        W = net.params[layer][0].data
        b = net.params[layer][1].data
#       plt.subplot(3, 1, i);
#       numBins = 2 ^ 8
#       plt.hist(W.flatten(), numBins, color='blue', alpha=0.8)
#       plt.show()
        print layer,
        print "kernel shape=", W.shape

        print 'W(%d) range = [%f, %f]' % (i, min(W.flatten()), max(W.flatten()))
        print 'W(%d) mean = %f, std = %f' % (i, np.mean(W.flatten()), np.std(W.flatten()))
        non_zero = (np.count_nonzero(W.flatten()) + np.count_nonzero(b.flatten()))
        all_param = (np.prod(W.shape) + np.prod(b.shape))
        this_layer_percentage = non_zero / float(all_param)
        total_nonzero += non_zero
        total_allparam += all_param
        print 'non-zero W and b cnt = %d' % non_zero
        print 'total W and b cnt = %d' % all_param
        print 'percentage = %f\n' % (this_layer_percentage)
        percentage_list.append(this_layer_percentage)


    print '=====> summary:'
    print 'non-zero W and b cnt = %d' % total_nonzero
    print 'total W and b cnt = %d' % total_allparam
    print 'percentage = %f' % (total_nonzero / float(total_allparam))
    print '=============analyze_param ends ==============='
    return (total_nonzero / float(total_allparam), percentage_list)


def analyze_data(net, layers):
    print '\n=============analyze_data start==============='
    for i, layer in enumerate(layers):
        D = net.blobs[layer].data
        print layer,
        print " data shape= ", D.shape
        print ' range = [%f, %f]' % (min(D.flatten()), max(D.flatten()))
        print ' mean = %f, std = %f' % (np.mean(D.flatten()), np.std(D.flatten()))
        non_zero = np.count_nonzero(D.flatten())
        all_param = np.prod(D.shape)
        this_layer_percentage = non_zero / float(all_param)
#         total_nonzero += non_zero
#         total_allparam += all_param
        print ' non-zero D cnt = %d' % non_zero
        print ' total D cnt = %d' % all_param
        print ' percentage = %f\n' % (this_layer_percentage)


folder = "/lenet5/"
folder = "/lenet_300_100/"
prototxt = caffe_root + '/3_prototxt_solver/' + folder + 'train_val.prototxt'
caffemodel = caffe_root + '/4_model_checkpoint/2_after_retrain/' + folder + 'best_pruned_lenet.caffemodel'
caffemodel = caffe_root + '/4_model_checkpoint/2_after_retrain/' + folder + 'best/best_relu.caffemodel'
caffemodel = './4_model_checkpoint/2_after_retrain/lenet5/best/best_lenet5_12x_conv.caffemodel'
caffemodel = './4_model_checkpoint/2_after_retrain/lenet_300_100/best/_iter_17500.caffemodel'
# layers = ['conv1', 'conv2', 'ip1', 'ip2']
layers = ['ip1', 'ip2', 'ip3']


net = caffe.Net(prototxt, caffemodel, caffe.TEST)
net.forward()
layers = net.params.keys()
blobs = net.blobs.keys()

analyze_param(net, layers)
analyze_data(net, blobs)

command = caffe_root + "/build/tools/caffe test --model=" + prototxt + " --weights=" + caffemodel + " --iterations=100 --gpu 0"
print command
os.system(command)


