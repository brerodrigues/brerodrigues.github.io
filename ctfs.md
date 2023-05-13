---
layout: page
permalink: /ctfs
permalink_name: /ctfs
title: CTFs writeups
---

# Write-ups de CTFs
`Alguns sem categoria definida e mais abaixo temos OverTheWire e HackTheBox.`

<strong>Sem Categoria</strong>
<ul>
{% for post in site.categories.CTFs %}
  {% if post.tags.size == 0 %}
  <p><a href="{{ post.url }}">{{ post.title }}</a> - <b>{{ post.date | date: "%b %-d, %Y" }}</b></p>

  {{ post.content | strip_html | truncatewords:20 }}
  {% endif %}
{% endfor %}
</ul>

{% for tag in site.tags %}
  {% assign t = tag[0] %}
  {% assign posts = tag[1] %}
  {% assign posts_with_tag = site.categories.CTFs | where_exp: "post", "post.tags contains t" %}
  {% assign first_tag_posts = posts_with_tag | where_exp: "post", "post.tags.first == t" %}
  {% if first_tag_posts.size > 0 %}
    <strong>{{ t }}</strong>
    <ul>
      {% for post in first_tag_posts %}
        <li>
          <a href="{{ post.url }}">{{ post.title }}</a> - <b>{{ post.date | date: "%b %-d, %Y" }}</b><br>
          {{ post.content | strip_html | truncatewords:20 }}
        </li>
      {% endfor %}
    </ul>
  {% endif %}
{% endfor %}


