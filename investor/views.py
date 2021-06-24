from django.shortcuts import render


# Create your views here.
# from . import SearchForm
# from BTech_Project_code.analysis.forms import 
from analysis.services import prepare_test_set
from .forms import SearchnumericForm
from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.http import JsonResponse
from sqlalchemy import create_engine
import pandas as pd
from numpy import argmax
import numpy as np
from datetime import timedelta
from datetime import date
from analysis.apps import DemoAppConfig
# Create your views here.


def home(request):
       #return render(request,"investor/home.html")
       '''
       if request.user.is_authenticated():
              return render(request,"investor/home.html")
       else:
              return render(request,"basic_app/login.html") 
       '''
       try:
              if request.session['username'] != None:
                     return render(request,"investor/home.html")
              else:
                     return redirect("login")
       except:
              return redirect("login")
       


def investorsearch(request):
   if request.is_ajax and request.method == "POST":
      #Get the posted form
      MySearchForm = SearchnumericForm(request.POST)

      if MySearchForm.is_valid():
         search_words = MySearchForm.cleaned_data['search_words']
            
         context = {
            'search_words' : search_words
            }
         search_words = search_words.lower()
         print("Query Searched: " ,search_words)
         #calling function from other .py file
         print(search_words)
        
         template = loader.get_template('investor/home.html')
        
         return HttpResponse(template.render(context, request))
         
   else:
      print("error")
      MySearchForm = SearchnumericForm()

   return render(request,'investor/home.html',{'search_form': MySearchForm})

def investor_numeric_prediction(request):
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
       
    
    
def recommendation(request):
    if request.is_ajax and request.method =="GET":

      # create sqlalchemy engine
       engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="",
                               db="text_data")) 
       model = DemoAppConfig.lstm
       model_prediction ={}
       
       company_list = ['amazon','google','apple','netflix','ibm','microsoft','facebook','tesla']
       
       for comp in company_list:
       
           table_rows_today = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-21' AND company= '"+comp+"'").fetchall()
           table_rows_yesterday = engine.execute("SELECT preprocessed_text FROM tweets_table WHERE date='2021-06-20' AND company= '"+comp+"'").fetchall()

           df_today = pd.DataFrame(table_rows_today, columns=['text'])
           df_yesterday = pd.DataFrame(table_rows_yesterday, columns=['text'])
       
           test_set_today = prepare_test_set(df_today)
           test_set_yesterday = prepare_test_set(df_yesterday) 
          
           predictions_today = (model.predict(test_set_today) > 0.65).astype("int32")
           predictions_yesterday =  (model.predict(test_set_yesterday) > 0.65).astype("int32")
          
           positive_count_1 = predictions_today.tolist().count([1])
           negative_count_1 = predictions_today.tolist().count([0])
          
           total_count_1 = positive_count_1+negative_count_1
           pos_percentage_1 = positive_count_1/total_count_1*100
         
           positive_count_2 = predictions_yesterday.tolist().count([1])
           negative_count_2 = predictions_yesterday.tolist().count([0])
           total_count_2 = positive_count_2+negative_count_2
           pos_percentage_2 = positive_count_2/total_count_2*100
          
           difference = (pos_percentage_1)-(pos_percentage_2)
           print(comp+':',difference)
       
           model_prediction[comp] = difference
       
       model_prediction = sorted(model_prediction.items(),key=lambda x:x[1])
       print(model_prediction)
       
       top1 = model_prediction[7][0]
       top2 = model_prediction[6][0]
       bottom1 = model_prediction[0][0]
       bottom2 = model_prediction[1][0]
       
       
       data ={"top1":top1, "top2":top2,"bottom1": bottom1,"bottom2": bottom2}
       return JsonResponse(data)

