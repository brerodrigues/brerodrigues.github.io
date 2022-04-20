---
layout: page
permalink: /favorites
permalink_name: /favorites
title: Posts favoritos
---

# Os melhores da casa de acordo com o Chef

{% for post in site.categories.Favorites %}
[{{ post.title }}]({{ site.url }}{{ post.url }}) - **{{ post.date | date: "%b %-d, %Y" }}**

{{ post.content | strip_html | truncatewords:20 }}
{% endfor %}