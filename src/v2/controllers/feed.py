from flask import Blueprint, Response
from flask_restful import Resource, Api
from time import localtime, gmtime, strftime
from v2.models.competitions import getList, getRelated
from v2.modules.feed_xml import feedWrapperCompetition
from v2.transformers.competition import transform


class FeedCompetition(Resource):
    def get(self):
        item = ""
        competitions = getList({
            "limit": 10,
            "orderby": "id_dsc"
        })

        # looping xml items
        for n in competitions['data']:
            n = transform(n)
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
                </item>
            """

        # return as feed rss
        # ref: https://stackoverflow.com/a/11774026/2780875
        return Response(feedWrapperCompetition(item, {
            "title": "Kompetisi Feed - Kompetisi Id",
            "desc": "Kompetisi terbaru di Kompetisi.id - Selalu Ada hadiah Setiap Hari"
        }), mimetype='text/xml')


api_feed_competition_bp = Blueprint('api_feed_competition', __name__)
api_feed_competition = Api(api_feed_competition_bp)
api_feed_competition.add_resource(FeedCompetition, '/v2/feed/competition')
