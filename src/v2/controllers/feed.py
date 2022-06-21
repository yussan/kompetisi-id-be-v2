from flask import Blueprint, Response
from flask_restful import Resource, Api
from time import localtime, strftime
import v2.models.competitions as CompetitionModel
import v2.models.news as NewsModel
from v2.modules.xml_template import feedTemplate
import v2.transformers.competition as CompetitionTransformer
import v2.transformers.news as NewsTransformer
import re

class FeedCompetition(Resource):
    def get(self):
        item = ""
        competitions = CompetitionModel.getList({
            "limit": 10,
            "orderby": "id_dsc",
            "status": "posted"
        })

        # looping xml items
        for n in competitions['data']:
            n = CompetitionTransformer.transform(n)

            link = "https://kompetisi.id/c/" + n["id"]

            # ref: split and join https://www.hackerrank.com/challenges/python-string-split-and-join/problem
            # ref: convert epoch to strftime
            item += """
                <item>
                <title>""" + n["title"] + """</title>
                <description>Selengkapnya di """ + link + """</description>
                <link>""" + link + """</link>
                <guid>""" + link + """</guid>
                <category domain="https://kompetisi.id">""" + "/".join(n["tag"].split(",")) + """</category>
                <pubDate>""" + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(float(n["created_at"]))) + """</pubDate>
                <comments>https://kompetisi.id/competition/""" + n["id"] + """/comments/""" + n["nospace_title"] + """</comments>
                <media:content url=\"""" + n["poster"]["original"] + """\" type="image/*" medium="image/jpeg" duration="10"> </media:content>
                </item>
            """

        # return as feed rss
        # ref: https://stackoverflow.com/a/11774026/2780875
        return Response(feedTemplate(item, {
            "title": "Kompetisi Feed - Kompetisi Id",
            "desc": "Kompetisi terbaru di Kompetisi.id - Selalu Ada hadiah Setiap Hari",
            "feed_link": "https://kompetisi.id/feed"
        }), mimetype='text/xml')


class FeedNews(Resource):
    def get(self):
        item = ""
        news = NewsModel.getList({
            "limit": 10,
            "status": "published"
        })

        for n in news["data"]:
            n = NewsTransformer.transform(n)

            link = "https://kompetisi.id/news/" + n["id"] + "/" + n["nospace_title"]
            
            item += """
                <item>
                <title>""" + n["title"] + """</title>
                <description>Selengkapnya di """ + link + """"</description>
                <link>""" + link  + """</link>
                <guid>""" + link + """/""" + n["nospace_title"] + """</guid>
                <category domain="https://kompetisi.id">""" + "/".join(n["tag"].split(",")) + """</category>
                <pubDate>""" + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(float(n["created_at"]))) + """</pubDate>
                <comments>https://kompetisi.id/news/""" + n["id"] + """/""" + n["nospace_title"] + """</comments>
                <media:content url=\"""" + n['image']['original']  + """\" type="image/*" medium="image/jpeg" duration="10"> </media:content>
                </item>
            """
        return Response(feedTemplate(item, {
            "title": "Berita Feed - Kompetisi Id",
            "desc": "Berita terbaru di Kompetisi.id - Selalu Ada hadiah Setiap Hari",
            "feed_link": "https://kompetisi.id/feed/news"
        }), mimetype='text/xml')


api_feed_competition_bp = Blueprint('api_feed_competition', __name__)
api_feed_news_bp = Blueprint('api_feed_news', __name__)

api_feed_competition = Api(api_feed_competition_bp)
api_feed_news = Api(api_feed_news_bp)

api_feed_competition.add_resource(FeedCompetition, '/v2/feed/competition')
api_feed_news.add_resource(FeedNews, '/v2/feed/news')
