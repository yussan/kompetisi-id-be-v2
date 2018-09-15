from flask import Blueprint, Response
from flask_restful import Resource, Api
from time import localtime, gmtime, strftime
from v2.helpers.strings import stripTags
import v2.models.competitions as CompetitionModel
import v2.models.news as NewsModel
from v2.modules.feed_xml import feedWrapperCompetition
import v2.transformers.competition as CompetitionTransformer
import v2.transformers.news as NewsTransformer


class FeedCompetition(Resource):
    def get(self):
        item = ""
        competitions = CompetitionModel.getList({
            "limit": 10,
            "orderby": "id_dsc"
        })

        # looping xml items
        for n in competitions['data']:
            n = CompetitionTransformer.transform(n)
            # ref: split and join https://www.hackerrank.com/challenges/python-string-split-and-join/problem
            # ref: convert epoch to strftime
            item += """
                <item>
                <title>""" + n["title"] + """</title>
                <description>""" + n["sort"] + """</description>
                <link>https://kompetisi.id/competition/""" + n["id"] + """/regulations/""" + n["nospace_title"] + """</link>
                <guid>https://kompetisi.id/competition/""" + n["id"] + """/regulations/""" + n["nospace_title"] + """</guid>
                <category domain="https://kompetisi.id">""" + "/".join(n["tag"].split(",")) + """</category>
                <pubDate>""" + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(float(n["created_at"]))) + """</pubDate>
                <comments>https://kompetisi.id/competition/""" + n["id"] + """/comments/""" + n["nospace_title"] + """</comments>
                </item>
            """

        # return as feed rss
        # ref: https://stackoverflow.com/a/11774026/2780875
        return Response(feedWrapperCompetition(item, {
            "title": "Kompetisi Feed - Kompetisi Id",
            "desc": "Kompetisi terbaru di Kompetisi.id - Selalu Ada hadiah Setiap Hari",
            "feed_link": "https://kompetisi.id/feed"
        }), mimetype='text/xml')

class FeedNews(Resource):
    def get(self):
        item = ""
        news = NewsModel.getList({
            "limit": 10
        })

        for n in news["data"]:
            n = NewsTransformer.transform(n)
            item += """
                <item>
                <title>""" + n["title"] + """</title>
                <description>""" + stripTags(n["content"]) + """</description>
                <link>https://kompetisi.id/news/""" + n["id"] + """/""" + n["nospace_title"] + """</link>
                <guid>https://kompetisi.id/news/""" + n["id"] + """/""" + n["nospace_title"] + """</guid>
                <category domain="https://kompetisi.id">""" + "/".join(n["tag"].split(",")) + """</category>
                <pubDate>""" + strftime("%a, %d %b %Y %H:%M:%S +0000", localtime(float(n["created_at"]))) + """</pubDate>
                <comments>https://kompetisi.id/news/""" + n["id"] + """/""" + n["nospace_title"] + """</comments>
                </item>
            """
        return Response(feedWrapperCompetition(item, {
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
