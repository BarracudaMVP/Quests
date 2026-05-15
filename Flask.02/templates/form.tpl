{% extends "base.tpl" %}

{% block content %}
<h2>{{it.Show()}}</h2>

<form action = '/add' method=POST>
<input type=hidden name=id value={{it.id}}>
Title:<input type=text name=title value={{it.title}}><br>
Author:<input type=text name=author value={{it.author}}>
<br><textarea name=body rows=10 cols=30 wrap=virtual>{{it.body}}</textarea>
<br><input type=submit value="Ok">
</form>

{% endblock %}