from django import forms
# 继承forms.Form
class LoginForm(forms.Form):
  # 如果为空则报错
  username = forms.CharField(required=True)
  # 同时也可以设定长度限制min_length、max_length
  password = forms.CharField(required=True, min_length=5)