
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


# Conventions to be follow
- Templates: A template for tool should be added to `tools/<category>/` under  `templates` folder. The template name should be in lowercase , use '_' instead of space.
For a tool name `Code Editor` the template name should be `code_editor.html`
- views.py:
  ## function based view
  def jpg_to_png_converter():
    //code
  ## class based view
  class UserProfileView():
      //code
- urls.py:
   # Its not required to append any url to the `urls.py`.The generic url for a tool is `/t/<url_endpoint>`, where `url_endpoint` value is defined by user while adding tool to database.
