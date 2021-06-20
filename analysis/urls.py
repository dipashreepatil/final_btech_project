from django.conf.urls import  url

from django.views.generic import TemplateView
from django.urls import path
from . import views

urlpatterns = [
    path('search_query/',views.search, name='search_view'),
    path('predict/',views.predict,name='predict'),
    path('past_predict/',views.past_predict, name="past_predict"),
    path('predictions_with_ML/', views.model, name="predict_with_model"),
    path('predictions_with_DL/',views.deep_learning_models, name="predict_with_deep_learning"),
    path('predictions_with_transformers/', views.transformer_models, name = 'predict_with_transformers'),
    path('numerical_predictions', views.numeric_prediction, name="numerical_prediction"),
    path('search_company/',views.companysearch, name='past_search_view'),
    path('past_predict/',views.past_predict,name='past_predict'),
    path('yearly_analysis/',views.yearly, name="yearly_prediction"),
    path('monthly_analysis/',views.monthly, name="monthly_prediction"),
    path('10k_analysis/',views.analysis_10k, name="10k_prediction"),
    path('compare_models/',views.model_comparision, name="model_comparision"),
    path('compare_ml_models/', views.model_comparision_ml , name="model_comparision_ml"),
    path('compare_dl_models/', views.model_comparision_dl , name="model_comparision_dl"),
    
     ]
