---
layout: page
permalink: /journal
permalink_name: /journal
title: Aleatoriedades
---

# Aleatoriedades nem sempre computacionais
`Eu sei lá.`

{% for post in site.categories.Rant %}
[{{ post.title }}]({{ site.url }}{{ post.url }}) - **{{ post.date | date: "%b %-d, %Y" }}**

{{ post.content | strip_html | truncatewords:20 }}
{% endfor %}
