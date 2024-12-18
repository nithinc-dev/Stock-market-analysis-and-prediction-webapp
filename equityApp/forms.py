# forms.py
from django import forms
from .models import *

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'placeholder': 'Type your message here...'}),
        }
class KeywordForm(forms.Form):
    keyword = forms.CharField(max_length=50,label='Enter a stock tiker keyword(eg. AAPL,MSFT for apple and microsoft)')


class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['email', 'keyword', 'price']
        labels = {
            'email': 'Email to get notified',
            'keyword': 'Stock Ticker',
            'price': 'Price which is more than or less than the current stock price',
            
        }
        
    # email = forms.EmailField(label='Enter your email address to get Notified')
    # keyword = forms.CharField(max_length=50,label='Enter a stock tiker keyword(eg. AAPL,MSFT for apple and microsoft)')
    # price = forms.PositiveIntegerField(label='Enter the stock price')
    
                             
# from django import forms

# from .models import *

# class StockForm(forms.ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['keyword']
        
# class MessageForm(forms.ModelForm):
#     class Meta:
#         model = Message 
#         fields = ['content']
        
# class KeywordForm(forms.ModelForm):
#     keyword = forms.ModelMultipleChoiceField(queryset=Stock.objects.all(), label="select a keyword")
    