{% extends "section.md" %}

{% block body %}
<table class="table table-hover">
{% for award in items %}
<tr>
  <td>
  <!-- <div style='float: right'>{{ award.year }}</div> -->
  <div>
    {{ award.title }}
    {% if award.link %}
        [<a href="{{ award.link }}">{{ "pre-print" }}</a>]
    {% endif %}
    {% if award.descr %}
    <br><p style="color:grey;font-size:1.4rem">{{ award.descr }}</p>
    {% endif %}
  </div>
  </td>
  <!-- <td class='col-md-2' style='text-align:right;'>{{ award.year }}</td> -->
</tr>
{% endfor %}
</table>
{% endblock body %}
