{% extends "base.tpl" %}

{% block content %}
    {% for it in items %}
{% include "item.tpl" ignore missing %}    
    {% else %}
Book is empty    
    {% endfor %}

{% include "add.tpl" ignore missing %}    
{% endblock %}