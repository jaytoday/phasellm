from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect

from .models import *

import json


def view_chat(request, chat_id):
    chats = ChatBotMessageArray.objects.filter(id=chat_id)

    if len(chats) != 1:
        return render(
            request,
            "view-chat.html",
            {
                "contenttitle": f"Viewing Chat ID {chat_id}",
                "error_msg": "Chat not found. Are you sure it exists?",
            },
        )

    return render(
        request,
        "view-chat.html",
        {
            "contenttitle": f"Viewing Chat ID {chat_id}",
            "json_message_array": json.dumps(chats[0].message_array),
            "chat_title": chats[0].title,
            "chat_id": chat_id,
        },
    )


def view_chat_new(request):
    new_chat = ChatBotMessageArray(message_array=[])
    new_chat.save()
    return redirect("view_chat", chat_id=new_chat.id)


# Same as createMessageArray() but we don't loads() from messages.
@require_http_methods(["POST"])
def createMessageArrayJson(request):
    data = json.loads(request.body)
    if "messages" in data:
        json_messages = data["messages"]
        cbma = ChatBotMessageArray(message_array=json_messages)
        if "title" in data:
            cbma.title = data["title"]
        cbma.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "message": "Unknown error."}, status=500)


@require_http_methods(["POST"])
def createMessageArray(request):
    data = json.loads(request.body)
    print(data)
    if "messages" in data:
        json_messages = json.loads(data["messages"])
        cbma = ChatBotMessageArray(message_array=json_messages)
        if "title" in data:
            cbma.title = data["title"]
        cbma.save()
        return JsonResponse({"status": "ok"})
    return JsonResponse({"status": "error", "message": "Unknown error."}, status=500)


@require_http_methods(["POST"])
def createJob(request):
    data = json.loads(request.body)

    title = ""
    if "title" in data:
        title = data["title"]

    message_collection_id = int(data["message_collection_id"])

    user_message = None
    if "user_message" in data:
        user_message = data["user_message"]

    mc_from_id = MessageCollection.objects.get(id=message_collection_id)

    b = BatchLLMJob(
        title=title,
        message_collection_id=message_collection_id,
        message_collection_ref=mc_from_id,
        user_message=user_message,
    )

    if "opt_gpt_4" in data:
        b.include_gpt_4 = data["opt_gpt_4"]

    if "opt_gpt_35" in data:
        b.include_gpt_35 = data["opt_gpt_35"]

    if "opt_temperature_scan" in data:
        b.temperature_range = data["opt_temperature_scan"]

    if "opt_num_runs" in data:
        b.run_n_times = data["opt_num_runs"]

    if "new_system_prompt" in data:
        if len(data["new_system_prompt"]) > 0:
            b.new_system_prompt = data["new_system_prompt"]

    if "opt_resend_user_msg" in data:
        b.resend_last_user_message = data["opt_resend_user_msg"]

    if "description" in data:
        if len(data["description"].strip()) > 0:
            b.description = data["description"].strip()

    b.save()

    return JsonResponse({"status": "ok"})


@require_http_methods(["POST"])
def createGroupFromCSV(request):
    data = json.loads(request.body)
    if "messagelist" in data:
        messages_csv = data["messagelist"]

        title = "New Collection"
        if "title" in data:
            title = data["title"]

        mc = MessageCollection(title=title, chat_ids=messages_csv.strip())

        chats_to_add = []

        ids = messages_csv.strip().split(",")
        all_present = True
        for chat_id in ids:
            o = ChatBotMessageArray.objects.filter(id=chat_id)
            if len(o) != 1:
                all_present = False
            chats_to_add.append(o[0])

        if all_present:
            mc.save()
            for c in chats_to_add:
                mc.chats.add(c)
            return JsonResponse({"status": "ok"})
        else:
            return JsonResponse(
                {
                    "status": "error",
                    "message": "Not all IDs are present in the data; please review and try again.",
                },
                status=500,
            )

    return JsonResponse({"status": "error", "message": "Unknown error."}, status=500)


def get_chats(request):
    all_chats = ChatBotMessageArray.objects.all().order_by("-created_at")
    return render(
        request, "chats.html", {"contenttitle": "Review Chats", "all_chats": all_chats}
    )


def list_groups(request):
    all_groups = MessageCollection.objects.all().order_by("-created_at")
    return render(
        request,
        "create-group.html",
        {
            "contenttitle": "Create Group",
            "contenttitle2": "Existing Groups",
            "all_groups": all_groups,
        },
    )


def list_jobs(request):
    all_jobs = BatchLLMJob.objects.all().order_by("-created_at")
    return render(
        request,
        "batch.html",
        {
            "contenttitle": "Create Job",
            "contenttitle2": "Job History",
            "all_jobs": all_jobs,
        },
    )


@require_http_methods(["POST"])
def update_title_via_post(request):
    data = json.loads(request.body)
    if "new_title" in data and "chat_id" in data:
        cid = int(data["chat_id"])
        chats = ChatBotMessageArray.objects.filter(id=cid)
        if len(chats) != 1:
            return JsonResponse(
                {"status": "error", "message": "Chat ID not found."}, status=500
            )
        else:
            chats[0].title = data["new_title"]
            chats[0].save()
            return JsonResponse({"status": "ok"})

    return JsonResponse(
        {"status": "error", "message": "Missing fields in request."}, status=500
    )


@require_http_methods(["POST"])
def overwrite_chat(request):
    data = json.loads(request.body)
    if "title" in data and "messages" in data and "chat_id" in data:
        cid = int(data["chat_id"])
        chats = ChatBotMessageArray.objects.filter(id=cid)
        if len(chats) != 1:
            return JsonResponse(
                {"status": "error", "message": "Chat ID not found."}, status=500
            )
        else:
            chats[0].title = data["title"]
            chats[0].message_array = data["messages"]
            chats[0].save()
            return JsonResponse({"status": "ok"})

    return JsonResponse(
        {"status": "error", "message": "Missing fields in request."}, status=500
    )


def review_jobs(request):
    jobs = BatchLLMJob.objects.all().order_by("-created_at")

    return render(
        request,
        "batch_review.html",
        {"contenttitle": "Review Batch Jobs", "jobs": jobs},
    )
