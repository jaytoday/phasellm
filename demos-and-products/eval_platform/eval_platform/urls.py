"""
URL configuration for eval_platform project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

import llmevaluator.views as lv

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", TemplateView.as_view(template_name="base-navigation.html")),
    path(
        "import",
        TemplateView.as_view(
            template_name="create.html",
            extra_context={"contenttitle": "Import Chat via JSON"},
        ),
    ),
    path("create_save_ma", lv.createMessageArray),
    path("create_save_ma_json", lv.createMessageArrayJson),
    path("groups", lv.list_groups),
    path("create_group_csv", lv.createGroupFromCSV),
    path("jobs", lv.list_jobs),
    path("create_job", lv.createJob),
    path("chats", lv.get_chats),
    path("view_chat/<int:chat_id>", lv.view_chat),
]
