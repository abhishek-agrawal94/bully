from django.shortcuts import render,redirect
from django import forms
from django.http import HttpResponseRedirect

from .forms import TextForm 

from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC

import sklearn.datasets
import sklearn.metrics
import sklearn.cross_validation
import sys
import os
import glob
import scipy.sparse as sp
import sklearn.feature_extraction.text
import sklearn.svm
from sklearn.feature_extraction.text import TfidfVectorizer
import csv
from django.shortcuts import render_to_response

# Create your views here.
from django.http import HttpResponse

def home(request):
   return render(request,'home.html',{})
   
def form(request):
	if request.method=="POST":
		form=TextForm(request.POST)
		if form.is_valid():
			text=form.cleaned_data['text']
			form.save(commit=True)
			return index(request)
	else :
		form=TextForm()
	print request.POST.get('text')
	lines = []
	lines1 = []
	with open("/home/ubuntu/Desktop/SVM/data_print") as f:
		for m in f:
                	lines.append(m.strip('\n').strip(" "))
	"""	
	with open("/home/ubuntu/Desktop/SVM/optional_data_print") as f1:
		for m1 in f1:
                	lines1.append(m1.strip('\n').strip(" "))
	"""
	return render(request,'form.html',{'form':lines,'form1':lines1})


def return_data(request):
	print "InNow"
	clf = sklearn.svm.LinearSVC()

	training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_training")
	f=open("/home/ubuntu/Desktop/SVM/dataset_prediction/test/test.txt",'w')
	fil=open("/home/ubuntu/Desktop/SVM/data_print",'a')
	fil.write("\n")
	text=request.POST.get('text')
	
	fil.close()
	f.write(text)
	f.close()
	print "Text ",text
	
	#print training_files.data

	predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM/dataset_prediction")

	print "Predict",predict_files.data

	vectorizer = TfidfVectorizer(encoding='utf-8')
	X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
	print("n_samples: %d, n_features: %d" % X_t.shape)
	assert sp.issparse(X_t)



	X_p = vectorizer.transform((open(f).read() for f in predict_files.filenames))

	print X_p
	clf.fit(X_t, training_files.target)
	y_predicted=""
	y_predicted = clf.predict(X_p)
	print "OUT",y_predicted
	if y_predicted[0]==0:
		
		f1=open("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/test.txt",'w')
		f1.write(text)
		f1.close()
		os.system("rm /home/ubuntu/Desktop/SVM_Multi/dataset_prediction/test/test.txt~")
		clf = sklearn.svm.LinearSVC()

		training_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_training")

		#print training_files.data

		predict_files = sklearn.datasets.load_files("/home/ubuntu/Desktop/SVM_Multi/dataset_prediction")

		print "Predict",predict_files.data

		vectorizer = TfidfVectorizer(encoding='utf-8')
		X_t = vectorizer.fit_transform((open(f).read() for f in training_files.filenames))
		print("n_samples: %d, n_features: %d" % X_t.shape)
		assert sp.issparse(X_t)
	
	


		X_p = vectorizer.transform((open(f).read()
		for f in predict_files.filenames))
		y1=OneVsOneClassifier(LinearSVC(random_state=0)).fit(X_t,training_files.target).predict(X_p)
		print y1
		if y1==0:
			fil=open("/home/ubuntu/Desktop/SVM/optional_data_print",'a')
			fil.write(text)
			fil.close()
		
			return render(request,'output.html',{'pred':"100 friends will view this post. Our system has detected harmful content which might hurt the user's sentiments.Are you sure you want to post this ?",'val':True,'text':text})
		elif y1==1:
			return render(request,'output.html',{'pred':"You have been temporarily banned till the moderator checks this post.Our system has detected harmful content which might hurt the user's sentiments. You cannot post another message until then. You can still continue to surf  ",'val':False})
		elif y1==2:
			return render(request,'output.html',{'pred':"Online help",'val':False})
	else:
		
		fil=open("/home/ubuntu/Desktop/SVM/data_print",'a')
		fil.write(text)
		fil.close()
		return HttpResponseRedirect("http://127.0.0.1:8000/HelloWorldApp/form/")
		#return render(request,'output.html',{'pred':"Dont be a noob",'val':0})
