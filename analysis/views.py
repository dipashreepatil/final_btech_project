from django.shortcuts import render


# Create your views here.
# from . import SearchForm
# from BTech_Project_code.analysis.forms import SearchForm
from .forms import SearchForm,CompanySearchForm
from django.template import loader
from django.http import HttpResponse
from .services import collect_news, collect_tweets,prepare_test_set,collect_stock_indices,collect_news
from django.shortcuts import render,redirect
from .apps import DemoAppConfig
from django.http import JsonResponse
from sqlalchemy import create_engine
import pandas as pd
from numpy import argmax
from transformers import pipeline
import numpy as np
from datetime import timedelta
from datetime import date


def search(request):
   if request.is_ajax and request.method == "POST":
      #Get the posted form
      MySearchForm = SearchForm(request.POST)

      if MySearchForm.is_valid():
         search_words = MySearchForm.cleaned_data['search_words']

         context = {
            'search_words' : search_words
            }
         search_words = search_words.lower()
         print("Query Searched: " ,search_words)
         #calling function from other .py file
         collect_stock_indices()
         print(search_words)
         collect_tweets(search_words+" stocks")
         collect_news(search_words)

         template = loader.get_template('analysis/predict.html')
        
         return HttpResponse(template.render(context, request))
         
   else:
      print("error")
      MySearchForm = SearchForm()

   return render(request,'analysis/predict.html',{'search_form': MySearchForm})



val=None
def companysearch(request):
       if request.is_ajax and request.method == "POST":
          #Get the posted form
              MySearchForm = CompanySearchForm(request.POST)
      

       if MySearchForm.is_valid():
              search_words = MySearchForm.cleaned_data['search_words']

              context = {
                     'search_words' : search_words
            }
              print("Query Searched: " ,search_words)
         #calling function from other .py file
              global val
              def val():
                     return search_words

              template = loader.get_template('analysis/pastanalysis.html')
        
              return HttpResponse(template.render(context, request))
         

       else:
              print("error")
              MySearchForm = SearchForm()

       return render(request,'analysis/pastanalysis.html',{'search_form': MySearchForm})


def predict(request):
       #return render(request,"analysis/predict.html")
       try:
              if request.session['username'] != None:
                     return render(request,"analysis/predict.html")
              else:
                     return redirect("login")
       except:
              return redirect("login") 

def past_predict(request):
       #return render(request, 'analysis/pastanalysis.html')
       try:
              if request.session['username'] != None:
                     return render(request,"analysis/pastanalysis.html")
              else:
                     return redirect("login")
       except:
              return redirect("login")
              
       


def model(request):
   if request.is_ajax and request.method == "GET":
      model_name = request.GET.get("model_name", None)
      company_name = request.GET.get("company",None)

      print(str(company_name))
      # create sqlalchemy engine
      engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
      today = date.today()
      yesterday = today - timedelta(days=1)
      company1=str(company_name)


      table_rows_today = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-21' AND company= '"+company1+"'").fetchall()
      table_rows_yesterday = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-20' AND company= '"+company1+"'").fetchall()

      table_rows_today_news = engine.execute("SELECT preprocessed_content FROM news_table WHERE date='2021-06-21' AND company= '"+company1+"'").fetchall()
      table_rows_yesterday_news = engine.execute("SELECT preprocessed_content FROM news_table WHERE date='2021-06-20' AND company= '"+company1+"'").fetchall()
 
      df_today = pd.DataFrame(table_rows_today, columns=['text'])
      df_yesterday = pd.DataFrame(table_rows_yesterday, columns=['text'])

      df_today_news = pd.DataFrame(table_rows_today_news, columns=['text'])
      df_yesterday_news = pd.DataFrame(table_rows_yesterday_news, columns=['text'])

      print("Length of dataframe(Today) : ", len(df_today))
      print("Length of dataframe(Yesterday) : ", len(df_yesterday))

      print("Length of dataframe(Today) : ", len(df_today_news))
      print("Length of dataframe(Yesterday) : ", len(df_yesterday_news))
      
      test_set_today = DemoAppConfig.cv_transformer.transform(df_today['text'])
      test_set_yesterday = DemoAppConfig.cv_transformer.transform(df_yesterday['text'])

      test_set_today_news = DemoAppConfig.cv_transformer.transform(df_today_news['text'])
      test_set_yesterday_news = DemoAppConfig.cv_transformer.transform(df_yesterday_news['text'])
      if model_name == "Logistic Regression":
             model = DemoAppConfig.logistic_regression
      elif model_name == "Perceptron":
             model = DemoAppConfig.perceptron
      elif model_name == "SVM":
             model = DemoAppConfig.svm
      elif model_name == "KNearest":
             model = DemoAppConfig.Kneighbors
      elif model_name == "ComplementNB":
             model = DemoAppConfig.complementNB
      elif model_name == "MultinomialNB":
             model = DemoAppConfig.multinomialNB
      elif model_name == "BernoulliNB":
             model = DemoAppConfig.bernoulliNB
      elif model_name == "Decision Tree":
             model = DemoAppConfig.dtree
      elif model_name == "Linear SVM":
             model = DemoAppConfig.linear_svc
      elif model_name == "Random Forest":
             model = DemoAppConfig.random_forest
      elif model_name == "AdaBoost":
             model = DemoAppConfig.adaboost
      elif model_name == "Gradient Descent":
             model = DemoAppConfig.gradient_boosting
      elif model_name == "SGD":
             model = DemoAppConfig.svm
          
      print("model: ", str(model))
    

      predictions_today = model.predict(test_set_today)
      predictions_yesterday =  model.predict(test_set_yesterday)
      
      predictions_today_news = np.where(model.predict_proba(test_set_today_news)[:,1]>0.7,1,0)
      predictions_yesterday_news =  np.where(model.predict_proba(test_set_yesterday_news)[:,1]>0.7,1,0)

      positive_count_1 = predictions_today.tolist().count(1)
      negative_count_1 = predictions_today.tolist().count(0)
      total_count_1 = positive_count_1+negative_count_1
      pos_percentage_1 = positive_count_1/total_count_1*100
      neg_percentage_1 = negative_count_1/total_count_1*100

      positive_count_1_news = predictions_today_news.tolist().count(1)
      negative_count_1_news = predictions_today_news.tolist().count(0)
      print(positive_count_1_news)
      print(negative_count_1_news)
      total_count_1_news = positive_count_1_news+negative_count_1_news
      pos_percentage_1_news = positive_count_1_news/total_count_1_news*100
      neg_percentage_1_news = negative_count_1_news/total_count_1_news*100

      positive_count_2 = predictions_yesterday.tolist().count(1)
      negative_count_2 = predictions_yesterday.tolist().count(0)
      total_count_2 = positive_count_2+negative_count_2
      pos_percentage_2 = positive_count_2/total_count_2*100
      neg_percentage_2 = negative_count_2/total_count_2*100

      positive_count_2_news = predictions_yesterday_news.tolist().count(1)
      negative_count_2_news = predictions_yesterday_news.tolist().count(0)
      total_count_2_news = positive_count_2_news+negative_count_2_news
      pos_percentage_2_news = positive_count_2_news/total_count_2_news*100
      neg_percentage_2_news = negative_count_2_news/total_count_2_news*100
      
      data_today = [pos_percentage_1,neg_percentage_1]
      data_yesterday = [pos_percentage_2,neg_percentage_2]

      data_today_news = [pos_percentage_1_news,neg_percentage_1_news]
      data_yesterday_news = [pos_percentage_2_news,neg_percentage_2_news]
      difference = (pos_percentage_1+pos_percentage_1_news)-(pos_percentage_2+pos_percentage_2_news)
      if(difference>0):
              direction=1
      else:
              direction=0
      chart_data ={"data_today":data_today, "data_yesterday":data_yesterday,"data_today_news": data_today_news,"data_yesterday_news": data_yesterday_news,"direction":direction}
      return JsonResponse(chart_data)


def yearly(request):
       if request.is_ajax and request.method == "GET":
          model_name = request.GET.get("model_name", None)
     
       if model_name == "Logistic Regression":
              model = DemoAppConfig.logistic_regression
       elif model_name == "Perceptron":
              model = DemoAppConfig.perceptron
       elif model_name == "SVM":
              model = DemoAppConfig.svm
       elif model_name == "KNearest":
              model = DemoAppConfig.Kneighbors
       elif model_name == "ComplementNB":
              model = DemoAppConfig.complementNB
       elif model_name == "MultinomialNB":
              model = DemoAppConfig.multinomialNB
       elif model_name == "BernoulliNB":
              model = DemoAppConfig.bernoulliNB
       elif model_name == "Decision Tree":
              model = DemoAppConfig.dtree
       elif model_name == "Linear SVM":
              model = DemoAppConfig.linear_svc
       elif model_name == "Random Forest":
              model = DemoAppConfig.random_forest
       elif model_name == "AdaBoost":
              model = DemoAppConfig.adaboost
       elif model_name == "Gradient Descent":
              model = DemoAppConfig.gradient_boosting
       elif model_name == "SGD":
              model = DemoAppConfig.svm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 

       company=val()
       print("Company= ",company)
       q1='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2020'

       table_rows20 = engine.execute(q1).fetchall()
       df20 = pd.DataFrame(table_rows20, columns=['text'])
       print("Length of dataframe : ", len(df20))
       total20=len(df20)
       test_set20 = DemoAppConfig.cv_transformer.transform(df20['text'])
       predictions20 = model.predict(test_set20)
       p20 = predictions20.tolist().count(1)
       n20 = predictions20.tolist().count(0)
       pos_20 = (p20/total20)*100
       neg_20 = (n20/total20)*100
       print(pos_20)
       print(neg_20)

       q2='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2019'
       table_rows19 = engine.execute(q2).fetchall()
       df19 = pd.DataFrame(table_rows19, columns=['text'])
       print("Length of dataframe : ", len(df19))
       total19=len(df19)
       test_set19 = DemoAppConfig.cv_transformer.transform(df19['text'])
       predictions19 = model.predict(test_set19)
       p19 = predictions19.tolist().count(1)
       n19 = predictions19.tolist().count(0)
       pos_19 = (p19/total19)*100
       neg_19 = (n19/total19)*100
       print(pos_19)
       print(neg_19)

       q3='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2018'
       table_rows18 = engine.execute(q3).fetchall()
       df18 = pd.DataFrame(table_rows18, columns=['text'])
       print("Length of dataframe : ", len(df18))
       total18=len(df18)
       test_set18 = DemoAppConfig.cv_transformer.transform(df18['text'])
       predictions18 = model.predict(test_set18)
       p18 = predictions18.tolist().count(1)
       n18 = predictions18.tolist().count(0)
       pos_18 = (p18/total18)*100
       neg_18 = (n18/total18)*100
       print(p18)
       print(n18)

       data2018=[pos_18,neg_18]
       data2019=[pos_19,neg_19]
       data2020=[pos_20,neg_20]

       #data_today = [pos_percentage_1,neg_percentage_1]
       #data_yesterday = [pos_percentage_2,neg_percentage_2]
       chart_data ={"data2018":data2018, "data2019":data2019, "data2020":data2020}
       return JsonResponse(chart_data)

def monthly(request):
       if request.is_ajax and request.method == "GET":
              model_name = request.GET.get("model_name", None)
     
       if model_name == "Logistic Regression":
              model = DemoAppConfig.logistic_regression
       elif model_name == "Perceptron":
              model = DemoAppConfig.perceptron
       elif model_name == "SVM":
              model = DemoAppConfig.svm
       elif model_name == "KNearest":
              model = DemoAppConfig.Kneighbors
       elif model_name == "ComplementNB":
              model = DemoAppConfig.complementNB
       elif model_name == "MultinomialNB":
              model = DemoAppConfig.multinomialNB
       elif model_name == "BernoulliNB":
              model = DemoAppConfig.bernoulliNB
       elif model_name == "Decision Tree":
              model = DemoAppConfig.dtree
       elif model_name == "Linear SVM":
              model = DemoAppConfig.linear_svc
       elif model_name == "Random Forest":
              model = DemoAppConfig.random_forest
       elif model_name == "AdaBoost":
              model = DemoAppConfig.adaboost
       elif model_name == "Gradient Descent":
              model = DemoAppConfig.gradient_boosting
       elif model_name == "SGD":
              model = DemoAppConfig.svm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data"))

       months=['01','02','03','04','05','06','07','08','09','10','11','12']
       positive=[]
       negative=[]
       company=val()

       for m in months:
              num=m
              query1="SELECT preprocessed_text FROM old_"+company+"_tweets1 WHERE YEAR(dates) = 2020 and MONTH(dates) ="+num
              table_rows19 = engine.execute(query1).fetchall()
              df = pd.DataFrame(table_rows19, columns=['text'])
              print("Length of dataframe : ", len(df))
              total=len(df)
              test_set = DemoAppConfig.cv_transformer.transform(df['text'])
              predictions = model.predict(test_set)
              p18 = predictions.tolist().count(1)
              n18 = predictions.tolist().count(0)
              pos = (p18/total)*100
              neg = (n18/total)*100
              positive.append(pos)
              negative.append(neg)

       print("Monthly positive: ",positive)
       print("Monthly negative: ",negative)
       chart_data1 ={"positive":positive, "negative":negative}
       return JsonResponse(chart_data1)


def analysis_10k(request):
       if request.is_ajax and request.method == "GET":
              model_name = request.GET.get("model_name", None)
     
       if model_name == "Logistic Regression":
              model = DemoAppConfig.logistic_regression
       elif model_name == "Perceptron":
              model = DemoAppConfig.perceptron
       elif model_name == "SVM":
              model = DemoAppConfig.svm
       elif model_name == "KNearest":
              model = DemoAppConfig.Kneighbors
       elif model_name == "ComplementNB":
              model = DemoAppConfig.complementNB
       elif model_name == "MultinomialNB":
              model = DemoAppConfig.multinomialNB
       elif model_name == "BernoulliNB":
              model = DemoAppConfig.bernoulliNB
       elif model_name == "Decision Tree":
              model = DemoAppConfig.dtree
       elif model_name == "Linear SVM":
              model = DemoAppConfig.linear_svc
       elif model_name == "Random Forest":
              model = DemoAppConfig.random_forest
       elif model_name == "AdaBoost":
              model = DemoAppConfig.adaboost
       elif model_name == "Gradient Descent":
              model = DemoAppConfig.gradient_boosting
       elif model_name == "SGD":
              model = DemoAppConfig.svm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data"))

       years=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
       positive10k=[]
       negative10k=[]
       
       for y in years:
              query1="SELECT text_final FROM 10k_text WHERE year="+y
              table_rows= engine.execute(query1).fetchall()
              df = pd.DataFrame(table_rows, columns=['text'])
              print("Length of dataframe : ", len(df))
              total=len(df)
              test_set = DemoAppConfig.cv_transformer.transform(df['text'])
              predictions = model.predict(test_set)
              p18 = predictions.tolist().count(1)
              n18 = predictions.tolist().count(0)
              pos = (p18/total)*100
              neg = (n18/total)*100
              positive10k.append(pos)
              negative10k.append(neg)

       print("10k yearly positive: ",positive10k)
       print("10k yearly negative: ",negative10k)
       chart_data2 ={"positive10k":positive10k, "negative10k":negative10k}
       return JsonResponse(chart_data2)



def deep_learning_models(request):
    if request.is_ajax and request.method =="GET":
       model_name = request.GET.get("model_name", None)
       company_name = request.GET.get("company",None)
      # create sqlalchemy engine
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
       company1=str(company_name)
       table_rows_today = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-21' AND company= '"+company1+"'").fetchall()
       table_rows_yesterday = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-20' AND company= '"+company1+"'").fetchall()

       table_rows_today_news = engine.execute("SELECT preprocessed_content FROM news_table WHERE date='2021-06-21' AND company= '"+company1+"'").fetchall()
       table_rows_yesterday_news = engine.execute("SELECT preprocessed_content FROM news_table WHERE date='2021-06-20' AND company= '"+company1+"'").fetchall()
 
       df_today = pd.DataFrame(table_rows_today, columns=['text'])
       df_yesterday = pd.DataFrame(table_rows_yesterday, columns=['text'])

       df_today_news = pd.DataFrame(table_rows_today_news, columns=['text'])
       df_yesterday_news = pd.DataFrame(table_rows_yesterday_news, columns=['text'])

       print("Length of dataframe(Today) : ", len(df_today))
       print("Length of dataframe(Yesterday) : ", len(df_yesterday))

       print("Length of dataframe(Today) : ", len(df_today_news))
       print("Length of dataframe(Yesterday) : ", len(df_yesterday_news))
      


       test_set_today = prepare_test_set(df_today)
       test_set_yesterday = prepare_test_set(df_yesterday) 
       test_set_today_news = prepare_test_set(df_today_news)
       test_set_yesterday_news = prepare_test_set(df_yesterday_news) 
       

       if model_name == "CNN":
             model = DemoAppConfig.cnn
       
       elif model_name == "Shallow RNN":
              model = DemoAppConfig.shallow_rnn
       
       elif model_name == "Deep RNN":
              model = DemoAppConfig.deep_rnn
       
       elif model_name == "Bidirectional RNN":
              model = DemoAppConfig.bidirectional_rnn

       elif model_name == "LSTM":
              model = DemoAppConfig.lstm

       predictions_today = (model.predict(test_set_today) > 0.75).astype("int32")
       predictions_yesterday =  (model.predict(test_set_yesterday) > 0.75).astype("int32")
      
       predictions_today_news = (model.predict(test_set_today_news) > 0.7).astype("int32")
       predictions_yesterday_news =  (model.predict(test_set_yesterday_news) > 0.7).astype("int32")
      
     
       positive_count_1 = predictions_today.tolist().count([1])
       negative_count_1 = predictions_today.tolist().count([0])
       print(positive_count_1)
       print(negative_count_1)

       total_count_1 = positive_count_1+negative_count_1
       pos_percentage_1 = positive_count_1/total_count_1*100
       neg_percentage_1 = negative_count_1/total_count_1*100

       positive_count_1_news = predictions_today_news.tolist().count([1])
       negative_count_1_news = predictions_today_news.tolist().count([0])
       print(positive_count_1_news)
       print(negative_count_1_news)

       total_count_1_news = positive_count_1_news+negative_count_1_news
       pos_percentage_1_news = positive_count_1_news/total_count_1_news*100
       neg_percentage_1_news = negative_count_1_news/total_count_1_news*100

       positive_count_2 = predictions_yesterday.tolist().count([1])
       negative_count_2 = predictions_yesterday.tolist().count([0])
       total_count_2 = positive_count_2+negative_count_2
       pos_percentage_2 = positive_count_2/total_count_2*100
       neg_percentage_2 = negative_count_2/total_count_2*100

       positive_count_2_news = predictions_yesterday_news.tolist().count([1])
       negative_count_2_news = predictions_yesterday_news.tolist().count([0])
       total_count_2_news = positive_count_2_news+negative_count_2_news
       pos_percentage_2_news = positive_count_2_news/total_count_2_news*100
       neg_percentage_2_news = negative_count_2_news/total_count_2_news*100
       
       data_today = [pos_percentage_1,neg_percentage_1]
       data_yesterday = [pos_percentage_2,neg_percentage_2]

       data_today_news = [pos_percentage_1_news,neg_percentage_1_news]
       data_yesterday_news = [pos_percentage_2_news,neg_percentage_2_news]
       difference = (pos_percentage_1+pos_percentage_1_news)-(pos_percentage_2+pos_percentage_2_news)
       if(difference>0):
              direction=1
       else:
              direction=0
       chart_data ={"data_today":data_today, "data_yesterday":data_yesterday,"data_today_news": data_today_news,"data_yesterday_news": data_yesterday_news,"direction":direction}
       return JsonResponse(chart_data)

def monthly_dl(request):
       if request.is_ajax and request.method == "GET":
              model_name = request.GET.get("model_name", None)
     
       if model_name == "CNN":
             model = DemoAppConfig.cnn
       
       elif model_name == "Shallow RNN":
              model = DemoAppConfig.shallow_rnn
       
       elif model_name == "Deep RNN":
              model = DemoAppConfig.deep_rnn
       
       elif model_name == "Bidirectional RNN":
              model = DemoAppConfig.bidirectional_rnn

       elif model_name == "LSTM":
              model = DemoAppConfig.lstm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data"))

       months=['01','02','03','04','05','06','07','08','09','10','11','12']
       positive=[]
       negative=[]
       company=val()

       for m in months:
              num=m
              query1="SELECT preprocessed_text FROM old_"+company+"_tweets1 WHERE YEAR(dates) = 2020 and MONTH(dates) ="+num
              table_rows19 = engine.execute(query1).fetchall()
              df = pd.DataFrame(table_rows19, columns=['text'])
              print("Length of dataframe : ", len(df))
              total=len(df)
              test_set = prepare_test_set(df)
              predictions = (model.predict(test_set) > 0.65).astype("int32")
              p18 = predictions.tolist().count([1])
              n18 = predictions.tolist().count([0])
              pos = (p18/total)*100
              neg = (n18/total)*100
              positive.append(pos)
              negative.append(neg)

       print("Monthly positive: ",positive)
       print("Monthly negative: ",negative)
       chart_data1 ={"positive":positive, "negative":negative}
       return JsonResponse(chart_data1)

def yearly_dl(request):
       if request.is_ajax and request.method == "GET":
          model_name = request.GET.get("model_name", None)
     
       if model_name == "CNN":
             model = DemoAppConfig.cnn
       
       elif model_name == "Shallow RNN":
              model = DemoAppConfig.shallow_rnn
       
       elif model_name == "Deep RNN":
              model = DemoAppConfig.deep_rnn
       
       elif model_name == "Bidirectional RNN":
              model = DemoAppConfig.bidirectional_rnn

       elif model_name == "LSTM":
              model = DemoAppConfig.lstm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 

       company=val()
       print("Company= ",company)
       q1='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2020'

       table_rows20 = engine.execute(q1).fetchall()
       df20 = pd.DataFrame(table_rows20, columns=['text'])
       print("Length of dataframe : ", len(df20))
       total20=len(df20)
       test_set20 = prepare_test_set(df20)
       predictions20 = (model.predict(test_set20) > 0.65).astype("int32")
       p20 = predictions20.tolist().count([1])
       n20 = predictions20.tolist().count([0])
       pos_20 = (p20/total20)*100
       neg_20 = (n20/total20)*100
       print(pos_20)
       print(neg_20)

       q2='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2019'
       table_rows19 = engine.execute(q2).fetchall()
       df19 = pd.DataFrame(table_rows19, columns=['text'])
       print("Length of dataframe : ", len(df19))
       total19=len(df19)
       test_set19 = prepare_test_set(df19)
       predictions19 = (model.predict(test_set19) > 0.65).astype("int32")
       p19 = predictions19.tolist().count([1])
       n19 = predictions19.tolist().count([0])
       pos_19 = (p19/total19)*100
       neg_19 = (n19/total19)*100
       print(pos_19)
       print(neg_19)

       q3='SELECT preprocessed_text FROM old_'+company+'_tweets1 WHERE YEAR(dates) = 2018'
       table_rows18 = engine.execute(q3).fetchall()
       df18 = pd.DataFrame(table_rows18, columns=['text'])
       print("Length of dataframe : ", len(df18))
       total18=len(df18)
       test_set18 = prepare_test_set(df18)
       predictions18 = (model.predict(test_set18) > 0.65).astype("int32")
       p18 = predictions18.tolist().count([1])
       n18 = predictions18.tolist().count([0])
       pos_18 = (p18/total18)*100
       neg_18 = (n18/total18)*100
       print(p18)
       print(n18)

       data2018=[pos_18,neg_18]
       data2019=[pos_19,neg_19]
       data2020=[pos_20,neg_20]

       #data_today = [pos_percentage_1,neg_percentage_1]
       #data_yesterday = [pos_percentage_2,neg_percentage_2]
       chart_data ={"data2018":data2018, "data2019":data2019, "data2020":data2020}
       return JsonResponse(chart_data)



def analysis_10k_dl(request):
       if request.is_ajax and request.method == "GET":
              model_name = request.GET.get("model_name", None)
     
       if model_name == "CNN":
             model = DemoAppConfig.cnn
       
       elif model_name == "Shallow RNN":
              model = DemoAppConfig.shallow_rnn
       
       elif model_name == "Deep RNN":
              model = DemoAppConfig.deep_rnn
       
       elif model_name == "Bidirectional RNN":
              model = DemoAppConfig.bidirectional_rnn

       elif model_name == "LSTM":
              model = DemoAppConfig.lstm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data"))

       years=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']
       positive10k=[]
       negative10k=[]
       
       for y in years:
              query1="SELECT text_final FROM 10k_text WHERE year="+y
              table_rows= engine.execute(query1).fetchall()
              df = pd.DataFrame(table_rows, columns=['text'])
              print("Length of dataframe : ", len(df))
              total=len(df)
              test_set = prepare_test_set(df)
              predictions = (model.predict(test_set) > 0.65).astype("int32")
              p18 = predictions.tolist().count([1])
              n18 = predictions.tolist().count([0])
              pos = (p18/total)*100
              neg = (n18/total)*100
              positive10k.append(pos)
              negative10k.append(neg)

       print("10k yearly positive: ",positive10k)
       print("10k yearly negative: ",negative10k)
       chart_data2 ={"positive10k":positive10k, "negative10k":negative10k}
       return JsonResponse(chart_data2)


def transformer_models(request):
       zero_shot_classifier = pipeline("zero-shot-classification")
       if request.is_ajax and request.method == "GET":

          model_name = request.GET.get("model_name", None)
          
      # create sqlalchemy engine
          engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                            .format(user="root",
                                   pw="",
                                   db="text_data")) 

          table_rows = engine.execute('SELECT preprocessed_text FROM tweets_table').fetchall()
          df = pd.DataFrame(table_rows, columns=['text'])
          print("Length of dataframe : ", len(df))

          tweets_list = df['preprocessed_text']
          sentiment_lst = ["Positive", "Negative"]
          scores_lst1 = []
          label_lst1 = []
          if model_name == 'ZSC':

              for statement in tweets_list:
                     results = zero_shot_classifier(statement, sentiment_lst)
                     SCORES = results["scores"]
                     CLASSES = results["labels"]
                     BEST_INDEX = argmax(SCORES)
                     predicted_class = CLASSES[BEST_INDEX]

                     scores_lst1.append(BEST_INDEX)
                     label_lst1.append(predicted_class)

              positives = 0
              negatives = 0

              for lb in df['Label']:
                     if lb == 'Positive':
                            positives += 1
                     else:
                            negatives += 1
              posperc = (positives/ (positives + negatives)) * 100
              negperc = (negatives/ (positives + negatives)) * 100

          data = [posperc,negperc]
          chart_data ={"data":data,}
          return JsonResponse(chart_data)

def corelation(request):
       if request.is_ajax and request.method == "GET":
              model_name = request.GET.get("model_name", None)
     
       
       model = DemoAppConfig.lstm
          
       print("model: ", str(model))
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data"))
       company=val()
       q1='SELECT preprocessed_text FROM old_'+company+'_tweets1 where YEAR(dates) = 2020'
       table_rows = engine.execute(q1).fetchall()
       df = pd.DataFrame(table_rows, columns=['text'])
       print("Length of dataframe : ", len(df))
       test_set = prepare_test_set(df)
       predictions = (model.predict(test_set) > 0.65).astype("int32")
       df['predictions'] = predictions

       q2='SELECT dates FROM old_'+company+'_tweets1 where YEAR(dates) = 2020'
       table_rowsd = engine.execute(q2).fetchall()
       df1 = pd.DataFrame(table_rowsd, columns=['date'])
       df['dates'] =df1

       engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="numeric_data"))
       
       q1='SELECT dates,close_p FROM old_'+company+'_data where YEAR(dates) = 2020'
       table_rowsn = engine1.execute(q1).fetchall()
       numeric_df = pd.DataFrame(table_rowsn, columns=['Date','Close'])
       date_list = numeric_df['Date']
       date_list = [x for x in date_list if str(x) != 'nan']
       
       positive_sentiment_list = [0]*len(date_list)
       negative_sentiment_list = [0]*len(date_list)
       total_list = [0]*len(date_list)
       for i in range(len(date_list)):
              temp_df = df[df.dates == date_list[i]]
              positive_sentiment_list[i] = temp_df['predictions'].tolist().count(1)
              negative_sentiment_list[i] = temp_df['predictions'].tolist().count(0)
              total_list[i] = temp_df['predictions'].count()


       pos_percent =[0]*len(total_list)
       neg_percent = [0] * len(total_list)
       for i in range(len(total_list)):
              pos_percent[i] = positive_sentiment_list[i]/total_list[i]*100
              neg_percent[i] = negative_sentiment_list[i]/total_list[i]*100
      
       sentiment_change = [0]*len(date_list)
       for i in range(1,len(date_list)):
              temp = pos_percent[i]-pos_percent[i-1]
              if temp > 0:
                     sentiment_change[i] = 1
              else:
                     sentiment_change[i] = -1

       percentage_change_list = [0]*len(numeric_df)
       actual_change = [0]*len(numeric_df)
       for i in range(1,len(numeric_df)):
              temp = (numeric_df.iloc[i]['Close']-numeric_df.iloc[i-1]['Close'])/numeric_df.iloc[i-1]['Close']*100
              percentage_change_list[i] = temp
              if temp > 0:
                     actual_change[i] = 1
              else: 
                     actual_change[i] = -1
       numeric_df['percentage_change'] = percentage_change_list
       numeric_df['actual_change'] = actual_change
       numeric_df['sentiment_change'] = sentiment_change
       numeric_df['actual_change'][0] = 1
       numeric_df['sentiment_change'][0] = 1

       date_list_1 = []
       sentiment_change_1=[]

       for i in range(len(numeric_df)):
              if(numeric_df['actual_change'][i]==numeric_df['sentiment_change'][i]):
                     date_list_1.append(numeric_df['Date'][i])
                     sentiment_change_1.append(numeric_df['percentage_change'][i])

       #new_list=[date_obj.strftime('%Y-%m-%d') for date_obj in date_list_1]
       #print("new list",new_list)

       chart_data ={"date_list":date_list,"percentage_change_list":percentage_change_list,"date_list_1":date_list_1, "sentiment_change_1":sentiment_change_1}
       return JsonResponse(chart_data)

def numeric_prediction(request):
    if request.is_ajax and request.method == "GET":
       company_name = request.GET.get("company", None)
       
       # create sqlalchemy engine
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                            .format(user="root",
                                   pw="",
                                   db="numeric_data")) 
       column='AMZN'
       sc = DemoAppConfig.AMZN_scalar
       model=DemoAppConfig.AMZN_LSTM                      
       company2=str(company_name)
       print("Company2: "+company2)
       if company2 == "amazon":
              column = 'AMZN'
              sc = DemoAppConfig.AMZN_scalar
              model=DemoAppConfig.AMZN_LSTM
       elif company2 == "google":
              column = 'GOOGL'
              sc = DemoAppConfig.GOOGL_scalar
              model = DemoAppConfig.GOOGL_LSTM
       elif company2 == "ibm":
              column = 'IBM'
              sc = DemoAppConfig.IBM_scalar
              model = DemoAppConfig.IBM_LSTM
       elif company2 == "microsoft":
              column = 'MSFT'
              sc = DemoAppConfig.MSFT_scalar
              model = DemoAppConfig.MSFT_LSTM
       elif company2 == "gamestop":
              column = 'GME'
              sc = DemoAppConfig.GME_scalar
              model = DemoAppConfig.GME_LSTM
       elif company2 == "tesla":
              column = 'TSLA'
              sc = DemoAppConfig.TSLA_scalar
              model = DemoAppConfig.TSLA_LSTM
       elif company2 == "facebook":
              column = 'FB'
              sc = DemoAppConfig.FB_scalar
              model = DemoAppConfig.FB_LSTM
       elif company2 == "apple":
              column = 'AAPL'
              sc = DemoAppConfig.AAPL_scalar
              model = DemoAppConfig.AMZN_LSTM
       elif company2 == "netflix":
              column = 'NFLX'
              sc = DemoAppConfig.NFLX_scalar
              model = DemoAppConfig.NFLX_LSTM
       elif company2 == "jp morgan":
              column = 'JPM'
              sc = DemoAppConfig.JPM_scalar
              model = DemoAppConfig.JPM_LSTM
       
       print(column)
       print(sc)
       print(model)
         
       query = "SELECT Datetime,"+column+" FROM ( SELECT * FROM stock_indices ORDER BY Datetime DESC LIMIT 20) sub ORDER BY Datetime ASC"
       table_rows = engine.execute(query).fetchall()
       df = pd.DataFrame(table_rows, columns=['Datetime','Indices'])
       
       inputs = df['Indices'][:20].values
       

       inputs = inputs.reshape(-1,1)
       

       datelist = df['Datetime'].dt.strftime("%Y-%m-%d %H:%m").tolist()
       print(datelist)
       

       inputs1 = sc.transform(inputs)
       test_set = []
       X_test = []
       for i in range(20,21):
              X_test.append(inputs1[i-20:i, 0])
              test_set.append(inputs[i-20:i, 0])
       test_set = test_set[0]
       l1 = test_set.tolist()
       X_test = np.array(X_test)


       X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
       predictions = model(X_test)
       predictions = sc.inverse_transform(predictions)
       predictions = predictions.tolist()
       print(test_set)
       print(predictions)
      
       chart_data ={"test_set":l1, "prediction":predictions, "datelist":datelist}
       return JsonResponse(chart_data)
       
def model_comparision_ml(request):
   if request.is_ajax and request.method == "GET":

       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
       rows = engine.execute("SELECT * FROM ml_model_performance").fetchall()
       df  = pd.DataFrame(rows,columns=['model','accuracy','precision','recall','f1_score','auc'])
       models = df['model'].tolist()
       accuracy = df['accuracy'].tolist()
       precision = df['precision'].tolist()
       recall = df['recall'].tolist()
       f1_score = df['f1_score'].tolist()
       auc = df['auc'].tolist()
       print(accuracy)
       chart_data ={"accuracy":accuracy ,"models":models, "precision":precision, "recall":recall , "f1_score":f1_score,"auc":auc}
       return JsonResponse(chart_data)

def model_comparision(request):
       try:
              if request.session['username']!=None:
                     return render(request,"analysis/modelcomparision.html")
              else:
                     return redirect("login")
       except:
              return redirect("login")
    
      
def model_comparision_dl(request):
   if request.is_ajax and request.method == "GET":

       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
       rows = engine.execute("SELECT * FROM dl_model_performance").fetchall()
       df  = pd.DataFrame(rows,columns=['model','accuracy','precision','recall','auc'])
       models = df['model'].tolist()
       accuracy = df['accuracy'].tolist()
       precision = df['precision'].tolist()
       recall = df['recall'].tolist()
       auc = df['auc'].tolist()
       print(accuracy)
       chart_data ={"accuracy":accuracy ,"models":models, "precision":precision, "recall":recall ,"auc":auc}
       return JsonResponse(chart_data)

def user_logout(request):
    try:
        del request.session['username']
        # return render(request,'basic_app/login.html')
        return redirect("login")

    except:
        del request.session['']
        return render(request,'basic_app/login.html')


      

