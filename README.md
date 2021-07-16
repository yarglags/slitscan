# slitscan
Some scripts I use in conjunction with ffmpeg to create slitscan images and videos.

Take a movie in slow motion in protrait orientation.

Cut a slice off column 1 of each frame and glue them all together to form an image.

Do the same with column 2, 3, ... until all the columns are turned into a load of images.

Make a movie with all the images.

I broke the task into two parts, greating the images and making the movie.

I'm learning ffmpeg and python the hard way. I'm sure the whole task could be done with a single ffmpeg command line but my brain will not bend that far. I'm also sure it could be done with python and the pillow library but where's the fun in that.

The code is not pretty but the images it profuces can be.
