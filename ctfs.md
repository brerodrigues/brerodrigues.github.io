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
  {{ tag }}
  {% assign t = tag | first %}
  {{ t }}
  {% assign posts = tag | last %}
  {% if desired_tags contains t %}
	<strong>{{ t }}</strong>
	<ul>
		{% for post in site.categories.CTFs %}
		{% if post.tags contains t %}
			<p><a href="{{ post.url }}">{{ post.title }}</a> - <b>{{ post.date | date: "%b %-d, %Y" }}</b></p>

		{{ post.content | strip_html | truncatewords:20 }}
		{% endif %}
		{% endfor %}
	</ul>
  {% endif %}
{% endfor %}



