---
show: true
width: 4
date: 2021-09-12 00:01:00 +0800
height: 295px
images:
- src: assets/images/baby.jpg
  title: Photo 1
  desc: Me in a village when I was 2-year-old.
- src: australia.jpg
  title: Photo 2
  desc: I was visiting my cousin in Australia.


{% include widgets/carousel.html id=page.id images=page.images height=page.height %}
