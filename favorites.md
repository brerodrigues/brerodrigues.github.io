---
layout: default
title: Favoritos
category: Favorites
permalink: category/favoritos/
---

{% for post in site.categories.Favorites %}
<li><a href="{{ site.url }}{{ post.url }}">{{ post.title }}</a></li>
{% endfor %}
