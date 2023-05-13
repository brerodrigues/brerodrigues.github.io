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

{% assign used_tags = "" %}

{% for post in site.categories.CTFs %}
  {% if post.tags.size > 0 %}
    {% assign first_tag = post.tags[0] %}
    
    {% unless used_tags contains first_tag %}
      {% assign used_tags = used_tags | append: first_tag | append: "|" %}
      
      <strong>{{ first_tag }}</strong>
      <ul>
        {% for post_with_tag in site.tags[first_tag] %}
          <li>
  <p><a href="{{ post_with_tag.url }}">{{ post_with_tag.title }}</a> - <b>{{ post_with_tag.date | date: "%b %-d, %Y" }}</b></p>

  {{ post_with_tag.content | strip_html | truncatewords:20 }}
          </li>
        {% endfor %}
      </ul>
    {% endunless %}
  {% endif %}
{% endfor %}





