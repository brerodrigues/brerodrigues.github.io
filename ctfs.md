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

{% assign desired_tags = ['Hack The Box', 'Leviathan OverTheWire', 'Narnia OverTheWire'] %}

{% for tag in site.tags %}
  {% assign t = tag[0] %}
  {% assign posts = tag[1] %}

  {% if desired_tags contains t %}
    <strong>{{ t }}</strong>
    <ul>
      {% for post in site.categories.CTFs %}
        {% if post.tags.size > 0 and post.tags[0] == t %}
          <li>
            <a href="{{ post.url }}">{{ post.title }}</a> - <b>{{ post.date | date: "%b %-d, %Y" }}</b><br>
            {{ post.content | strip_html | truncatewords:20 }}
          </li>
        {% endif %}
      {% endfor %}
    </ul>
  {% endif %}
{% endfor %}


