---
layout: page
permalink: /rant
permalink_name: /rant
title: Aleatoriedades
---

# Aleatoriedades nem sempre computacionais

{% for post in site.categories.Rant %}
[{{ post.title }}]({{ site.url }}{{ post.url }}) - **{{ post.date | date: "%b %-d, %Y" }}**

{{ post.content | strip_html | truncatewords:20 }}
{% endfor %}