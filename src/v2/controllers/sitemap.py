from flask import Blueprint, Response
from flask_restful import Resource, Api
import v2.models.competitions as CompetitionModel
import v2.models.news as NewsModel
import v2.transformers.competition as CompetitionTransformer
import v2.transformers.news as NewsTransformer
from v2.modules.xml_template import sitemapTemplate
from v2.helpers.datetime import epochToFormat

# sitemap template format : https://www.sitemaps.org/protocol.html


class SitemapCompetition(Resource):
    def get(self):
        # get latest 200 posts as sitemap
        items = ""
        competitions = CompetitionModel.getList({
            "limit": 10,
            "orderby": "id_dsc"
        })

        # looping to generate xml chilld
        for n in competitions['data']:
            n = CompetitionTransformer.transform(n)

            items += """
              <url>
                <loc>https://kompetisi.id/competition/""" + n["id"] + """/regulations/""" + n["nospace_title"] + """</loc>
                <lastmod>""" + epochToFormat(n["updated_at"], "%Y-%m-%d") + """</lastmod>
                <changefreq>monthly</changefreq>
                <priority>0.9</priority>
            </url>
            """
        # end of looping

        return Response(sitemapTemplate(items, {
        }), mimetype='text/xml')


class SitemapNews(Resource):
    def get(self):
        # get latest 200 posts as sitemap
        items = ""
        news = NewsModel.getList({
            "limit": 200
        })

        # looping to generate xml chilld
        for n in news['data']:
            n = NewsTransformer.transform(n)
            items += """
              <url>
                <loc>https://kompetisi.id/news/""" + n["id"] + """/""" + n["nospace_title"] + """</loc>
                <lastmod>""" + epochToFormat(n["updated_at"], "%Y-%m-%d") + """</lastmod>
                <changefreq>monthly</changefreq>
                <priority>0.9</priority>
            </url>
            """

        return Response(sitemapTemplate(items, {
        }), mimetype='text/xml')


api_sitemap_competition_bp = Blueprint('api_sitemap_competition', __name__)
api_sitemap_news_bp = Blueprint('api_sitemap_news', __name__)

api_sitemap_competition = Api(api_sitemap_competition_bp)
api_sitemap_news = Api(api_sitemap_news_bp)

api_sitemap_competition.add_resource(
    SitemapCompetition, '/v2/sitemap/competition')
api_sitemap_news.add_resource(SitemapNews, '/v2/sitemap/news')
