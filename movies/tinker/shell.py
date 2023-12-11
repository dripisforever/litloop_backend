from imdb import Cinemagoer
cinemagoer = Cinemagoer()
imdb_id = 'tt1442449'
imdb_id = imdb_id.replace('tt', '')
movie = cinemagoer.get_movie(imdb_id)
plot = movie.get('plot')
plot = movie.get('plot')

mv = Movie(
    title=title,
    description=plot
)
mv.save()
