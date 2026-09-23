---
layout: page
title: Projects & Experiments
subtitle: Tools, research and prototypes across Ethereum, institutional infrastructure and AI-enabled operations.
permalink: /projects/
---

<p class="projects-intro">A working portfolio of ideas and experiments. Entries marked “Illustrative concept” are examples of areas to develop; links and screenshots will be added as projects are ready to share.</p>

<div class="project-grid">
  {% for project in site.data.projects %}
    {% assign project_index = forloop.index %}
    {% include project-card.html project=project index=project_index %}
  {% endfor %}
</div>
