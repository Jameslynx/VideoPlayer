"""
########################################################
# tmdb_api.py:
# get Movie and Tv data from themoviedatabase.org;
# using my API key and tmdbsimple
########################################################
"""
import json
import tmdbsimple as tmdb
from collections import defaultdict

info_dict = defaultdict(list)
# tmdb.API_KEY = {YOUR TMDB API}
YOURL = "https://www.youtube.com/watch_popup?v={}&vq=hd1080"


class Movies(tmdb.Movies):
    """Sub-class of tmdb.Movies"""

    def __init__(self, *args, **kwargs):
        """initialize class attributes"""
        super(Movies, self).__init__(*args, **kwargs)
        self.popular_movies = self.popular()
        self.top_rated_movies = self.top_rated()
        self.upcoming_movies = self.upcoming()
        self.now_playing_movies = self.now_playing()
        self.info_dict = defaultdict(list)
        self.post_url_base = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'

    def info_packer(self, key, obj):
        """Pack movie information into info_dict"""
        for mv in obj['results']:
            mv_info = {'title': mv['title']}
            mv_info['poster'] = self.post_url_base + mv['poster_path']
            id_ = mv['id']
            self.id = id_
            trailer_info = []
            for info in self.videos()['results']:
                trailer_info.append(
                    [info['name'],YOURL.format(info['key']), info['site']]
                )
            mv_info['trailers'] = trailer_info
            self.info_dict[key].append(mv_info)

    def info_populate(self):
        """Pass data to info_packer"""
        key_obj = [('upcoming', self.upcoming_movies),
                   ('now_playing', self.now_playing_movies),
                   ('popular', self.popular_movies),
                   ('top_rated', self.top_rated_movies)]
        for key, obj in key_obj:
            self.info_packer(key, obj)

class TV(tmdb.TV):
    """Sub-class of tmdb.Movies"""

    def __init__(self, *args, **kwargs):
        """initialize class attributes"""
        super(TV, self).__init__(*args, **kwargs)
        self.popular_tv= self.popular()
        self.top_rated_tv = self.top_rated()
        self.on_the_air_tv = self.on_the_air()
        self.info_dict = defaultdict(list)
        self.post_url_base = 'https://image.tmdb.org/t/p/w600_and_h900_bestv2'

    def info_packer(self, key, obj):
        """Pack tv information into info_dict"""
        for tv in obj['results']:
            tv_info = {'title': tv['name']}
            tv_info['poster'] = self.post_url_base + tv['poster_path']
            id = tv['id']
            self.id = id
            trailer_info = []
            for info in self.videos()['results']:
                trailer_info.append(
                    [info['name'],YOURL.format(info['key']), info['site']]
                )
            tv_info['trailers'] = trailer_info
            self.info_dict[key].append(tv_info)

    def info_populate(self):
        """Pass data to info_packer"""
        key_obj = [('on_the_air', self.on_the_air_tv),
                   ('popular', self.popular_tv),
                   ('top_rated', self.top_rated_tv)]
        for key, obj in key_obj:
            self.info_packer(key, obj)


if __name__ == '__main__':
    movies = Movies()
    movies.info_populate()
    tv = TV()
    tv.info_populate()
    all_trailers = {"movies": movies.info_dict, "tv": tv.info_dict}

    import os
    mod = __import__(__name__)
    path = __name__.split('.')
    for p in path[1:]:
        mod = getattr(mod, p)
    dirname = os.path.dirname(mod.__file__)
    with open(os.path.join(dirname, 'trailers.json'), 'w') as f_obj:
        json.dump(all_trailers, f_obj, sort_keys=True, indent=4)
