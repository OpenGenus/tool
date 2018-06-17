
# Adding Tools

- Create a template for tool under `templates/tools/` with following format
```
{% extends "tools/tool_base.html" %}
{% load staticfiles %}

{% block tool %}
{% endblock %}

{% block scripts %}
{% endblock %}

```
- Login to Admin Panel and add tool, fill in author, template name, url_endpoint and other info regarding the tool.

- For client side tool, the logic for the tool has to be written in javascript in the template itself. Below is an example:

  ```
    function capitalize() {
      var text = $('#inputtextarea').val().toUpperCase();
      $('#outputtextarea').val(text);
    }
  ```

- For server side tool, create a new view and register url for the same. The logic for the tool will be in the views.py file.
    ```
    # views.py
    def convert_file(request):
        #logic here

      return response

   # urls.py
   urlpatterns = [
     ...
     url(r'^convert_file/$',
            views.convert_file,
            name='convert_file'),
     ...
      ]
    ```
