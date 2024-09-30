from django import forms
from app.models import Job_finder,Employer, Comment, Post, CV

class EUpdateForm(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ['company_name', 'address', 'city', 'introduction']

class JFUpdateForm(forms.ModelForm):
    class Meta:
        model = Job_finder
        fields = ['full_name','gender','address', 'city', 'introduction']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Write a comment'}),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['pic_url', 'caption','contact', 'address', 'field','job', 'description', 'hour', 'salary', 'approve', 'deny']
        widgets = {
            'caption' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'contact' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'address' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'field' : forms.Select(attrs={'class':'form-select'}),
            'job' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'description' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'hour' : forms.Textarea(attrs={'class':'form-control','style':'width:500px','style':'height:100px'}),
            'salary' : forms.Select(attrs={'class':'form-select'}),
            'approve' : forms.Textarea(attrs={'class':'form-control'}),
            'deny' : forms.Textarea(attrs={'class':'form-control'})
        }

class CVForm(forms.ModelForm):
    # Additional fields for company_name and job_applied
    company_name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    job_applied = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'form-control'}))
    
    class Meta:
        model = CV
        fields = ['introduction', 'experience', 'education', 'interest', 'languages', 'skill', 'mail', 'phone']
        widgets = {
            'introduction' : forms.Textarea(attrs={'class':'form-control'}),
            'experience' : forms.Textarea(attrs={'class':'form-control'}),
            'education' : forms.Textarea(attrs={'class':'form-control'}),
            'interest' : forms.Textarea(attrs={'class':'form-control'}),
            'languages' : forms.Textarea(attrs={'class':'form-control'}),
            'skill' : forms.Textarea(attrs={'class':'form-control'}),
            'mail' : forms.EmailInput(attrs={'class':'form-control'}),
            'phone' : forms.NumberInput(attrs={'class':'form-control', 'onkeydown':"return event.keyCode !== 69"})
        }