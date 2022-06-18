import srt

class Subtitles:
    
    def __init__(self, movie_name):
        self.movie_name = movie_name
        file = open('./{}/subtitles.srt'.format(movie_name), 'r').read()
        subtitle_generator = srt.parse(file)
        self.subtitles = list(subtitle_generator)
        
    def get_start_time(self, index):
        return self.subtitles[index].start
    
    def get_end_time(self, index):
        return self.subtitles[index].end
    
    def get_content(self, index):
        return self.subtitles[index].content
    
    def get_subtitles(self):
        return [subtitle.content for subtitle in self.subtitles]
    
    def time_interval_to_subtitle(self, start_time, end_time):
        subtitle_found = False
        
        num_subtitles = len(self.subtitles)
        start_index = 0
        end_index = num_subtitles - 1
        subtitle_guess_index = int((start_index + end_index) / 2)
        subtitle_guess_index_old = -1
        
        while (start_index < end_index):
            subtitle_guess_index = int((start_index + end_index) / 2)
            subtitle_guess = self.subtitles[subtitle_guess_index]
            
            if (subtitle_guess_index == subtitle_guess_index_old):
                return int(subtitle_guess.index)
            elif (end_time < subtitle_guess.start.total_seconds()):
                end_index = subtitle_guess_index
            elif (start_time > subtitle_guess.end.total_seconds()):
                start_index = subtitle_guess_index
            else:
                return int(subtitle_guess.index)
            subtitle_guess_index_old = subtitle_guess_index
        
        return subtitle_guess_index
            
# test_srt_object = Subtitles('Harry_Potter_and_the_Sorcerers_Stone')
# print(test_srt_object.get_subtitles())