import environ
from pprint import pprint
from notion2md.exporter.block import MarkdownExporter, StringExporter
import markdown
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

env = environ.Env()
env.read_env('.env')
NOTION_TOKEN = env('NOTION_TOKEN')

class TopView(generic.TemplateView):
    template_name = "welcome/top.html"

class OverviewView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="09fe43f0a19541c7ac96310828bd3f79"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)
    
class AttentionView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="b6660c7bf0a5435d8531ed7ee73990e9"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)
    
class WhatView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="658d2bb791ba4d69aecadd48463e76cc"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)
    
class MinorView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="7a4efe8084474fc5ac7f2e1e553da798"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)
    
class TimetableView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="9c2b689027e94096979ac51e9b81f1c1"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)
    
class ExampleTimetableView(generic.TemplateView):
    template_name = "welcome/page.html"
    def get(self, request, **kwargs):
        BLOCK_ID="83942579c182414b81a4df45382522e5"
        md = StringExporter(block_id=BLOCK_ID).export()
        extentions = ['tables', 'markdown_checklist.extension', 'markdown_strikethrough.extension']
        html = markdown.markdown(md, extensions=extentions).replace("table", 'table class="ui celled table unstackable"')
        text = html
        context = {
            'items': text
        }
        #print(text)
        return self.render_to_response(context)