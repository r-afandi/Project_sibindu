from django.urls import path
from ...views.data_pakar.v_data_pakar import PakarListView, UpdatePakarView, DeletePakarView,InputPakar,TrainNaiveBayesView
app_name ='data_pakar'
urlpatterns = [
    path('', PakarListView.as_view(), name='data_pakar'),
    path('add/', PakarListView.as_view(), name='add_pakar'),
    path('edit/<int:id>/', UpdatePakarView.as_view(), name='edit_pakar'),
    path('input/<int:id>/', InputPakar.as_view(), name='input_pakar'),
    path('train/', TrainNaiveBayesView.as_view(), name='train_pakar'),
    path('update/<int:id>/', UpdatePakarView.as_view(), name='update_pakar'),
    path('delete/<int:id>/', DeletePakarView.as_view(), name='delete_pakar'),
    # ... other URL patterns
]
