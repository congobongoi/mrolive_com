from django import forms
    
class WODashboardForm(forms.Form):
    wo_number = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'placeholder': '100072-E79-22-001...','id':'wo_number'}))
    date_from = forms.DateTimeField(required=False,widget=forms.DateTimeInput(attrs={'id':'date_from'}))
    date_to = forms.DateTimeField(required=False,widget=forms.DateTimeInput(attrs={'id':'date_to'}))
    due_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'placeholder': '02/23/2020','id':'due_date'}))
    get_due_date = forms.DateField(required=False,widget=forms.DateInput(attrs={'placeholder': '02/23/2020','id':'get_due_date'}))
    location = forms.CharField(required=False,max_length=25,widget=forms.TextInput(attrs={'placeholder': 'WIP...','id':'location'}))
    warehouse = forms.CharField(required=False,max_length=25,widget=forms.TextInput(attrs={'placeholder': 'CA07...','id':'warehouse'}))
    customer = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'placeholder': 'Bonaero Engineering...','id':'customer'}))
    manager = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder': 'GGREEN...','id':'manager'}))
    get_manager = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder': 'KBURRELL...','id':'manager'}))
    rank = forms.CharField(required=False,max_length=20,widget=forms.TextInput(attrs={'placeholder': '15...','id':'rank'}))
    rack = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'placeholder': 'CART 07...','id':'rack'}))
    user_id = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'id':'user_id'},render_value=True))
    
    def clean(self):
        cleaned_data = super().clean()
        wo_number = cleaned_data.get("wo_number")
        date_from = cleaned_data.get("date_from")
        date_to = cleaned_data.get("date_to")
        due_date = cleaned_data.get("due_date")
        get_due_date = cleaned_data.get("get_due_date")
        location = cleaned_data.get("location")
        warehouse = cleaned_data.get("warehouse")
        customer = cleaned_data.get("customer")
        manager = cleaned_data.get("manager")
        get_manager = cleaned_data.get("get_manager")
        rank = cleaned_data.get("rank")
        rack = cleaned_data.get("rack")
        user_id = cleaned_data.get("user_id")
    
class PIUpdateForm(forms.Form):
    stock_label = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'placeholder': '100750000001...','id':'wo_number'}))
    quantity = forms.FloatField(required=False,widget=forms.TextInput(attrs={'placeholder': '77...','id':'quantity'}))
    batch_no = forms.CharField(required=False,max_length=50,widget=forms.TextInput(attrs={'placeholder': '30002...','id':'batch_no'}))
    user_id = forms.CharField(required=False,widget=forms.PasswordInput(attrs={'id':'user_id'},render_value=True))