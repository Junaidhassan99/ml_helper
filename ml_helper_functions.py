# -*- coding: utf-8 -*-
"""ml_helper_functions.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-f7uBKlB152WzAbNIQG9_q9qJfNdAKKd
"""

import tensorflow as tf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

import os
from os import walk

def get_file_names(dir_path):

  """
  It will return a list of file names from a directory,
  for example getting class names from directory
  """

  return sorted(os.listdir(dir_path))

import random

def grid_view_img_data(imgs, labels, class_names = [], row = 2, col = 2, figsize=(8,8)):

  """
  Display random images with labels in a grid form
  from given list of images and respective labels

  imgs: must be normalized (1/225.)

  example 1:
  for imgs, labels in train_data.take(1):
    grid_view_img_data(imgs/255.,labels)
  """

  plt.figure()
  f, axarr = plt.subplots(row,col,figsize=figsize)

  for i in range(row):
    for j in range(col):
      img_index=random.randint(0, len(imgs)-1)
      axarr[i,j].imshow(imgs[img_index], cmap='gray', vmin=0, vmax=255)

      if class_names != []:
        axarr[i,j].set_title(class_names[int(labels[img_index])])
      else:
        axarr[i,j].set_title(int(labels[img_index]))


import datetime

def create_tensorboard_callback(dir_name, experiment_name):

  """
  Create a Tensorboard callback with a file name having
  directory name, experiment name and datetime of creation
  to saves logs of model training
  """

  # the place where we want to save performace logs
  log_dir = dir_name +'/' + experiment_name + '/' + datetime.datetime.now().strftime('%Y%m%d-%H%M%S')

  return tf.keras.callbacks.TensorBoard(log_dir = log_dir)

def plot_loss_curve(model_fit):

  """
  It will plot a graph with loss and accuracy on vertical
  and epochs on horizontal axis

  model_fit: an object returned by fit function of tensorflow
  """

  pd.DataFrame(model_fit.history).plot()

  plt.ylabel('metrices')
  plt.xlabel('epochs')


import itertools
from sklearn.metrics import confusion_matrix

def matplotlib_confusion_matrix(y_true, y_pred,figsize=(5, 5), class_names = None, text_size=20):

  """
  Note: The following confusion matrix code is a remix of Scikit-Learn's
  plot_confusion_matrix function - https://scikit-learn.org/stable/modules/generated/sklearn.metrics.plot_confusion_matrix.html
  and Made with ML's introductory notebook - https://github.com/GokuMohandas/MadeWithML/blob/main/notebooks/08_Neural_Networks.ipynb
  """

  y_test=y_true
  y_preds=y_pred

  # figsize = (5, 5)

  # Create the confusion matrix
  cm = confusion_matrix(y_test, y_preds)
  cm_norm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis] # normalize it
  n_classes = cm.shape[0]

  # Let's prettify it
  fig, ax = plt.subplots(figsize=figsize)
  # Create a matrix plot
  cax = ax.matshow(cm, cmap=plt.cm.Blues) # https://matplotlib.org/3.2.0/api/_as_gen/matplotlib.axes.Axes.matshow.html
  fig.colorbar(cax)

  if class_names:
    labels = class_names
  else:
    labels = np.arange(cm.shape[0])

  # Label the axes
  ax.set(title="Confusion Matrix",
         xlabel="Predicted label",
         ylabel="True label",
         xticks=np.arange(n_classes),
         yticks=np.arange(n_classes),
         xticklabels=labels,
         yticklabels=labels)

  # Set x-axis labels to bottom
  ax.xaxis.set_label_position("bottom")
  ax.xaxis.tick_bottom()

  # Adjust label size
  ax.xaxis.label.set_size(text_size)
  ax.yaxis.label.set_size(text_size)
  ax.title.set_size(text_size)

  # Set threshold for different colors
  threshold = (cm.max() + cm.min()) / 2.

  # Plot the text on each cell
  for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
    plt.text(j, i, f"{cm[i, j]} ({cm_norm[i, j]*100:.1f}%)",
             horizontalalignment="center",
             color="white" if cm[i, j] > threshold else "black",
             size=text_size)

import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

def sns_confusion_matrix(Y_true, Y_pred, figsize=(5, 5), class_names = None, label_size=1.4, text_size=16):

  cm = confusion_matrix(Y_true, Y_pred)
  # Normalise
  cmn = (cm.astype('float') / cm.sum(axis=1)[:, np.newaxis])*100
  fig, ax = plt.subplots(figsize=figsize)
  sns.set(font_scale=label_size) # for label size
  sns.heatmap(cmn, annot=True, fmt='.2f', annot_kws={"size": text_size}, xticklabels=class_names, yticklabels=class_names)
  plt.ylabel('Actual')
  plt.xlabel('Predicted')
  plt.show(block=False)


# Calculate the time of predictions
import time
def pred_timer(model, samples):
  """
  Times how long a model takes to make predictions on samples.
  
  Args:
  ----
  model = a trained model
  sample = a list of samples

  Returns:
  ----
  total_time = total elapsed time for model to make predictions on samples
  time_per_pred = time in seconds per single sample
  """
  start_time = time.perf_counter() # get start time
  model.predict(samples) # make predictions
  end_time = time.perf_counter() # get finish time
  total_time = end_time-start_time # calculate how long predictions took to make
  time_per_pred = total_time/len(samples) # find prediction time per sample
  return total_time, time_per_pred


def time_series_window_horizon_split(list_a, window_size, horizon_size):

  """
  Takes a time series, divides it into equal chuncks of 
  (window_size + horizon_size), then further splits each
  chunk into windows and horizons and return them separately
  as numpy arrays 
  """

  def split(list_a, chunk_size):

    for i in range(0, len(list_a), chunk_size):
      yield list_a[i:i + chunk_size]

  chunk_size = window_size + horizon_size
  split_array = list(split(list_a, chunk_size))

  if split_array[0].shape != split_array[-1].shape:
    split_array = np.stack(split_array[:-1], axis=0)
  else:
    split_array = np.stack(split_array, axis=0)

  windows = [i[:-1] for i in split_array]
  horizons = [i[-1] for i in split_array]

  return np.array(windows), np.array(horizons)
