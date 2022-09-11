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

def grid_view_img_data_gen(batch_imgs, class_names = [], row = 2, col = 2, figsize=(8,8)):

  # calling next on image data will return images equal to batch we have assigned
  imgs, labels = batch_imgs.next()

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
