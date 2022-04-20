---
layout: page
permalink: /hacking
permalink_name: /hacking
title: Hacking posts
---

# Hacking e derivados
`Das vezes que tentei hackear uns negócios aí e resolvi contar a história.`

{% for post in site.categories.Hacking %}
[{{ post.title }}]({{ site.url }}{{ post.url }}) - **{{ post.date | date: "%b %-d, %Y" }}**

{{ post.content | strip_html | truncatewords:20 }}
{% endfor %}

<!-- {{ post.content | strip_html | truncatewords:20 }} -->
<!-- {{ post.excerpt }} -->