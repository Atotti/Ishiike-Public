from dataclasses import field
from xml.etree.ElementTree import Comment
from django import forms
from django.core.mail import EmailMessage

from .models import Question, QComment, Faculty, Department


class QuestionModelForm(forms.ModelForm):
    faculty = forms.ModelChoiceField(queryset=Faculty.objects.all(), empty_label='選択してください')
    department = forms.ModelChoiceField(queryset=Department.objects.none(), empty_label='選択してください')

    class Meta:
        model = Question
        fields = [
            'faculty',
            'department',
            'content',
            'tag',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tag'].empty_label = '選択して下さい'
        self.fields['faculty'].empty_label = '選択してください'
        self.fields['department'].empty_label = '選択してください'
        self.fields['faculty'].label = '学部'
        self.fields['department'].label = '学科'

        if self.instance.pk:
            self.fields['department'].queryset = self.instance.faculty.department_set.order_by('department')

        self.fields['faculty'].widget.attrs.update({
            'class': 'form-control',
            'id': 'faculty-select',
        })

        self.fields['department'].widget.attrs.update({
            'class': 'form-control',
            'id': 'department-select',
        })

    class Media:
        js = ('js/question_form.js',)



class CommentModelForm(forms.ModelForm):
    class Meta:
        model = QComment
        fields = [
            'comment'
        ]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)