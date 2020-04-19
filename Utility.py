import time
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV

from sklearn.metrics import precision_recall_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve

##################################################################################################################

# Funtion to give missing value details of the table
def miss(table):
    miss = table.isnull().sum()
    miss = miss[miss>0]
#     miss.sort_values(inplace=True)
    return miss
    

##################################################################################################################

# Function to return similarity score between the two data
def sim_score(a,b):
    dot = np.dot(a, b)
    norma = np.linalg.norm(a)
    normb = np.linalg.norm(b)
    cos = dot / (norma * normb)
    return cos

##################################################################################################################

# Merging d1 & d2
def merge(d1,d2,on,how):
    d = pd.merge(d1,d2,on=on,how=how)
    return d

##################################################################################################################

# Removing NaN and converting the df columns to int type
def remove_NaN_convert_int(d,col,con_int):
    d = d.drop(columns = col,axis=1)
    if con_int:
        d.fillna(0,inplace=True)
    return d

##################################################################################################################
    
# clf is model
# train_X is the train dataset without target used for taking out feature names
def feature_importance(clf,predictor,figsize):
    feat_importances = pd.Series(clf.feature_importances_, index=predictor).sort_values(ascending=True)
    feat_importances.plot(kind='barh',figsize=figsize)
    plt.show()
    feat_importances = pd.DataFrame(feat_importances).reset_index().sort_values(by=0,ascending=False)
    feat_importances = feat_importances.rename(columns={'index':'feature_name',0:'score'})
    return feat_importances


##################################################################################################################

# summarize results
def grid_search_result(grid_result):
  print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
  params = grid_result.cv_results_['params']
  means_test = grid_result.cv_results_['mean_test_score']
  stds_test = grid_result.cv_results_['std_test_score']
  means_train = grid_result.cv_results_['mean_train_score']
  stds_train = grid_result.cv_results_['std_train_score']
  for param, mean_test, stdev_test, mean_train, stdev_train in zip(params, means_test, stds_test, means_train, stds_train):
    print("With following parameter: %r" % (param),end=' ')
    print("Test_auc_score: %f (%f)" % (mean_test, stdev_test),end=' ')
    print("Train_auc_score: %f (%f)" % (mean_train, stdev_train))


##################################################################################################################

def classification_report_(X_test,y_test,y_pred,model):
    confusion_mat = confusion_matrix(y_test, y_pred)
    print('Confusion_Matrix: ',confusion_mat,sep='\n')
    print()
    print('Accuracy of classifier on test set: {:.2f}'.format(model.score(X_test, y_test)))
    print()
    
    # Classification Report
    print('Classification Report: ')
    print(classification_report(y_test, y_pred))
    print()
    
##################################################################################################################

from sklearn import metrics
def precision_recall_curve_(X_test,y_test,y_score_test):
    from sklearn.metrics import precision_score,recall_score
    threshold = np.arange(0,1,0.001)
    precision = np.zeros(len(threshold))
    recall = np.zeros(len(threshold))
    f1_score = np.zeros(len(threshold))
    for i in range(len(threshold)):
        y1 = np.zeros(len(y_score_test),dtype=int)
        y1 = np.where(y_score_test<=threshold[i],0,1)
        precision[i] = metrics.precision_score(y_test,y1,zero_division=0)
        recall[i] = metrics.recall_score(y_test,y1,zero_division=0)
        f1_score[i] = metrics.f1_score(y_test,y1,zero_division=0)
    sns.set_style('whitegrid')
    sns.lineplot(x=threshold,y=precision)
    sns.lineplot(x=threshold,y=recall)
    sns.lineplot(x=threshold,y=f1_score)
    plt.xlabel('Threshold')
    plt.ylabel('Value')
    plt.legend(['precision','recall','f1_score'])
    plt.show()

##################################################################################################################

def roc_auc(X_test,y_test,y_pred,model):
    confusion_mat = confusion_matrix(y_test, y_pred)
    print('Confusion_Matrix: ',confusion_mat,sep='\n')
    print()
    print('Accuracy of classifier on test set: {:.2f}'.format(model.score(X_test, y_test)))
    print()
    
    # Classification Report
    print('Classification Report: ')
    print(classification_report(y_test, y_pred))
    y_score = model.predict_proba(X_test)[:,1]              # Predicted probability score
    fpr, tpr, thresholds = roc_curve(y_test, y_score)

    # calculate the g-mean for each threshold
    gmeans = np.sqrt(tpr * (1-fpr))
    # locate the index of the largest g-mean
    ix = np.argmax(gmeans)
    print('Best Threshold=%f, G-Mean=%.3f' % (thresholds[ix], gmeans[ix]))
    print()
    
    plt.figure()
    # AuC Score & plotting of AuC curve
    plt.plot(fpr, tpr, label='AuC score (area = %0.2f)' % roc_auc_score(y_test, y_score))
    plt.scatter(fpr[ix], tpr[ix], marker='o', color='black', label='Best')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic')
    plt.legend(loc="lower right")
    plt.show()
    
##################################################################################################################

def compare_train_test_AUC(X_train,y_train,X_test,y_test,model):
  y_score_train = model.predict_proba(X_train)[:,1]
  y_score_test = model.predict_proba(X_test)[:,1]              # Predicted probability score
  fpr_train, tpr_train, thresholds_train = roc_curve(y_train, y_score_train)
  fpr_test, tpr_test, thresholds_test = roc_curve(y_test, y_score_test)
  # calculate the g-mean for each threshold
  gmeans_train = np.sqrt(tpr_train * (1-fpr_train))
  gmeans_test = np.sqrt(tpr_test * (1-fpr_test))
  # locate the index of the largest g-mean
  ix_train = np.argmax(gmeans_train)
  ix_test = np.argmax(gmeans_test)
  print('Best Train threshold=%f, G-Mean=%.3f' % (thresholds_train[ix_train], gmeans_train[ix_train]))
  print('Best Test threshold=%f, G-Mean=%.3f' % (thresholds_test[ix_test], gmeans_test[ix_test]))
  print()
      
  plt.figure()
  # AuC Score & plotting of AuC curve
  plt.plot(fpr_train, tpr_train, label='Train AuC score (area = %0.2f)' % roc_auc_score(y_train, y_score_train))
  plt.plot(fpr_test, tpr_test, label='Test AuC score (area = %0.2f)' % roc_auc_score(y_test, y_score_test))
  plt.scatter(fpr_train[ix_train], tpr_train[ix_train], marker='o', color='black', label='Best_threshold')
  plt.scatter(fpr_test[ix_test], tpr_test[ix_test], marker='o', color='black')
  plt.plot([0, 1], [0, 1],'r--')
  plt.xlim([0.0, 1.0])
  plt.ylim([0.0, 1.05])
  plt.xlabel('False Positive Rate')
  plt.ylabel('True Positive Rate')
  plt.title('Receiver operating characteristic')
  plt.legend(loc="lower right")
  plt.show()
    
##################################################################################################################

def precision_recall(X_test,y_test,clf):
  # predict probabilities
  y_score = clf.predict_proba(X_test)[:,1]

  # calculate roc curves
  precision, recall, thresholds = precision_recall_curve(y_test, y_score)
  # convert to f score
  fscore = (2 * precision * recall) / (precision + recall)
  # locate the index of the largest f score
  ix = np.argmax(fscore)
  print('Best Threshold=%f, F-Score=%.3f' % (thresholds[ix], fscore[ix]))

  # plot the roc curve for the clf
  no_skill = len(y_test[y_test==1]) / len(y_test)
  pyplot.plot([0,1], [no_skill,no_skill], linestyle='--', label='No Skill')
  pyplot.plot(recall, precision, marker='.', label='Logistic')
  pyplot.scatter(recall[ix], precision[ix], marker='o', color='black', label='Best')
  # axis labels
  pyplot.xlabel('Recall')
  pyplot.ylabel('Precision')
  pyplot.legend()
  plt.show()

##################################################################################################################

def check_accuracy_number_ones(test_X,test_y,model,count_1,title_plot):
    # Range: 0.023899981073654975 0.9522668197195199
    threshold = [x/400 for x in range(0,380)]
    # check how many of class 1 are actually matching correctly
    y_score = model.predict_proba(test_X)[:,1]

    correct = [0]*len(threshold)
    matching_pos_class = [0]*len(threshold)
    s = ['*']*len(threshold)
    print('Total no of observation: %f',len(y_score))
    print(*s,sep='')
    for th in range(len(threshold)):
        y_pred = [1 if x>=threshold[th] else 0 for x in y_score]
        correct[th] = ((test_y==y_pred)).sum()/len(y_score)
        matching_pos_class[th] = ((test_y==y_pred) & (y_pred==np.ones(len(y_pred)))).sum()/count_1
        print(*s[th],end='')
    # print(th,threshold[th],correct[th],matching_pos_class[th])
    print()
    plt.figure(figsize=(9,6))
    sns.set_style(style='whitegrid')
    plt.plot(threshold,correct)
    plt.plot(threshold,matching_pos_class)
    plt.title(title_plot)
    plt.legend(['accuracy','No of correct ones predicted'])
    plt.show()