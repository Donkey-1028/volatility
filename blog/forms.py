from django import forms
from .models import *

CHOICES = [
    ('author', '작성자'),
    ('title', '제목'),
    ('content', '내용'),
           ]


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['created_date', 'update_date']
        #fields = ['author', 'password', 'title', 'content'] 와 같은의미

        #bootstrap에 맞는 class를 사용하기위해 widgets에서 form의 class를 정의해놓음.
        widgets = {
            'author': forms.TextInput(
                attrs={'class': 'form-control'}
            ),
            'password': forms.PasswordInput(
                attrs={'class': 'form-control', 'placeholder': 'Your Password'}
            ),
            'title': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Title'}
            ),
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Content'}
            ),

        }

    def clean_author(self):
        """author가 admin인 것은 관리자이기 때문에 사용자는
        admin을 사용하지 못하게 하는 메소드.
        author필드를 확인"""
        cd = self.cleaned_data
        if cd['author'] == 'admin':
            raise forms.ValidationError("'admin'이라는 닉네임 사용하지 마세요.")
        return cd['author']


class SearchForm(forms.Form):
    search_type = forms.ChoiceField(choices=CHOICES, widget=forms.Select, label='')
    search_word = forms.CharField(label='Search Word')


class PasswordCheck(forms.Form):
    check_password = forms.CharField(max_length=10, widget=forms.PasswordInput(attrs={'id': 'check_password'}), label="작성시 사용한 비밀번호 입력하세요")


class CommentForm(forms.ModelForm):
    password = forms.CharField(label='Password', max_length=10, widget=forms.PasswordInput(attrs={'size': 8}))

    class Meta:
        model = Comment
        exclude = ['post', 'create_date']
        widgets = {
            'author': forms.TextInput(attrs={'size': 8}),
            'comment': forms.TextInput(attrs={'size': 35})
        }

    def clean_author(self):
        """author가 admin인 것은 관리자이기 때문에 사용자는
        admin을 사용하지 못하게 하는 메소드.
        author필드를 확인"""
        cd = self.cleaned_data
        if cd['author'] == 'admin':
            raise forms.ValidationError("'admin'이라는 닉네임 사용하지 마세요.")
        return cd['author']