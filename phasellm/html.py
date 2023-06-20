"""
Support for convering LLM-related classes and objects to HTML and various outputs.
"""

import re

# Easier to have this variable than to escape all the "{" and "}" later.
style = """
.phasellm_chatbot_stream {
    margin:5px;
    box-sizing:content-box;
    padding:8px;
    border-radius:8px;
    border:1px solid black;
    display:inline-block;
}
.phasellm_chatbot_stream .response_container {
    display:block;
    display:block;
    margin:5px;
    padding:8px;
}

.content_user {
    background-color:green;
    color:white;
}

.content_system {
    color:gray;
    background-color:lightgray;
    font-style:italic;
}

.content_assistant {
    color:white;
    background-color:crimson;
}

.response {
    padding:8px;
    border-radius:8px;  
}

.phasellm_chatbot_stream .timestamp {
    margin:5px 5px 5px 15px;
    font-size:70%;
    color:gray;
    font-style:italic;
    display:inline-block;
}

.phasellm_chatbot_stream .time_taken {
    margin:5px 5px 5px 15px;
    font-size:70%;
    color:gray;
    font-style:italic;
    display:inline-block;
}

.legend {
    font-size:70%;
    text-align:right;
    padding-right:15px;
}

.legend_box {
    width:10px;
    height:10px;
    display:inline-block;
    position:relative;
    top:2px;
    margin-left:8px;
    margin-right:2px;
}
"""

def _formatContentToHtml(string):
    """
    Converts a String into an HTML-friendly representation.
    """
    new_string = re.sub("<", "&lt;", string)
    new_string = re.sub(">", "&gt;", string)
    new_string = re.sub('[\r\n]+', '<br>', new_string)
    return new_string

def toHtmlFile(html, filepath):
    """
    Takes an html object generated by PhaseLLM and saves it to an HTML file.
    """

    html_content = f"""
<!doctype html>
<html lang="en">
<head>
<style>
{style}
</style>
</head>
<body>
{html}
</body>
</html>
    """
    with open(filepath, 'w') as w:
        w.write(html_content)


def chatbotToHtml(chatbot):
    """
    Converts a chatbot's message stack to HTML.
    """

    chatbot_html = """<div class='phasellm_chatbot_stream'>
<div class="legend">
    <b>Legend</b><div class="legend_box content_system">&nbsp;</div> System <div class="legend_box content_assistant">&nbsp;</div> Assistant <div class="legend_box content_user">&nbsp;</div> User
</div>"""

    messages = chatbot.messages
    for m in messages:

        m_timestamp = ""
        if "timestamp_utc" in m:
            m_timestamp = m['timestamp_utc'].strftime("%d %B %Y at %H:%M:%S")
        
        m_log_time_seconds_string = ""
        if "log_time_seconds" in m:
            m_log_time_seconds_string = f"""<div class='time_taken'>({str(round(m['log_time_seconds'], 3))} seconds)</div>"""
            
        response_html = f"""
<div class='response_container'>
    <div class='response content_{m['role']}'>{_formatContentToHtml(m['content'])}</div>
    <div class='timestamp'>{m_timestamp}</div>
    {m_log_time_seconds_string}
</div>
"""

        chatbot_html += response_html

    chatbot_html += "\n</div>"

    return chatbot_html