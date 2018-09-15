from time import gmtime, strftime

def feedWrapperCompetition(items = '', params={}):
  # ref: strftime https://docs.python.org/3.3/library/time.html?highlight=time.strftime#time.strftime
  return """<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
      <channel>
        <title>""" + (params["title"] if "title" in params else "Kompetisi Id Feed")  + """</title>
        <description>""" + (params["desc"] if "desc" in params else "Selalu ada hadiah setiap hari")  + """</description>
        <link>https://kompetisi.id</link>
        <category domain="https://kompetisi.id">kompetisi/lomba/kontes/sayembara</category>
        <copyright>Copyright 2017-2018 Id More Team.</copyright>
        <lastBuildDate>""" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + """</lastBuildDate>
        <language>en-us</language>
        <image>
          <url>https://res.cloudinary.com/dhjkktmal/image/upload/v1528851826/kompetisi-id/email_assets/icon-512x512.png</url>
          <title>""" + (params["title"] if "title" in params else "Kompetisi Id Feed")  + """</title>
          <link>https://kompetisi.id</link>
          <description>""" + (params["desc"] if "desc" in params else "Selalu ada hadiah setiap hari")  + """</description>
          <width>400</width>
          <height>400</height>
        </image>
        <atom:link href="https://kompetisi.id/feed" rel="self" type="application/rss+xml" />
        """ + items + """
      </channel>
    </rss>"""