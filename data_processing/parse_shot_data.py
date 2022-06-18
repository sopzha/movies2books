import csv

class Shots:
    
    def __init__(self, movie_name):
        self.movie_name = movie_name
        file = open('./{}/movie_scenes.csv'.format(movie_name))
        
        csvreader = csv.reader(file)
        
        next(csvreader)    # Skip headers
        next(csvreader)
       
        self.shots = []
        for shot in csvreader:
            self.shots.append(shot)
            
        file.close()
        
    def time_interval_to_shot(self, start_time, end_time):
        shot_found = False
        
        num_shots = len(self.shots)
        start_index = 0
        end_index = num_shots - 1
        shot_guess_index = int((start_index + end_index) / 2)
        
        while (start_index < end_index):
            shot_guess_index = int((start_index + end_index) / 2)
            shot_guess = self.shots[shot_guess_index]
            if (end_time < float(shot_guess[3])):
                end_index = shot_guess_index
            elif (start_time > float(shot_guess[6])):
                start_index = shot_guess_index
            else:
                return int(shot_guess[0])
            
# movie_shots = Shots('American_Psycho')
# print(movie_shots.time_interval_to_shot(322, 324))
