import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from parse_shot_data import Shots

SHOT_NEIGHBORHOOD = 5
PARAGRAPH_NEIGHBORHOOD = 5

def timestamp_to_seconds(timestamp):
    [hours, minutes, seconds] = timestamp.split(':')
    return 3600 * float(hours) + 60 * float(minutes) + float(seconds)

def compute_ground_truth(book_name):
    
    original_ground_truth = json.load(open('./{}/ground_truth_annotation.json'.format(book_name)))
    
    image_features = np.asarray(np.load('./{}/shot_features.npy'.format(book_name)).T, dtype = np.float64)
    image_features /= np.linalg.norm(image_features, axis=0, keepdims=True)
    image_features = image_features[:, 0:image_features.shape[1]:3]    # 3 frames per shot
    
    text_features = np.asarray(np.load('./{}/paragraph_features.npy'.format(book_name)).T, dtype = np.float64)
    text_features /= np.linalg.norm(text_features, axis=0, keepdims=True)
    
    number_shots = image_features.shape[1]    
    number_paragraphs = text_features.shape[1]
        
    shot_data = Shots(book_name)
    
    new_ground_truth = []
    original_alignment_scores = []
    new_alignment_scores = []
    
    for alignment in original_ground_truth:
        
        [start_timestamp, end_timestamp] = alignment['Time Shot'].split(' ')
        start_time = timestamp_to_seconds(start_timestamp)
        end_time = timestamp_to_seconds(end_timestamp)
        current_shot = shot_data.time_interval_to_shot(start_time, end_time) - 1   # shots start at 1, adjust for indexing
        
        shot_interval_start = max(0, current_shot - SHOT_NEIGHBORHOOD)
        shot_interval_end = min(number_shots, current_shot + SHOT_NEIGHBORHOOD)
        shot_interval = np.array([shot for shot in range(shot_interval_start, shot_interval_end)])
        
        paragraph_interval_start = max(0, alignment['id_paragraph'] - PARAGRAPH_NEIGHBORHOOD)
        paragraph_interval_end = min(number_paragraphs, alignment['id_paragraph'] + PARAGRAPH_NEIGHBORHOOD)
        paragraph_interval = np.array([paragraph for paragraph in range(paragraph_interval_start, paragraph_interval_end)])
        
        matrix = text_features[:, paragraph_interval].T @ image_features[:, shot_interval]
        # (10, 512) x (512, 10) = (10, 10)
        
        matrix_coordinates = np.unravel_index(np.argsort(matrix, axis=None)[::-1], matrix.shape)
        
        paragraph_index = matrix_coordinates[0][0]
        shot_index = matrix_coordinates[1][0]
        alignment_type = [int('Dialog' in alignment['Alignment Type']), int('Visual' in alignment['Alignment Type']), int('Sound' in alignment['Alignment Type'])]
        
#         assert(0 < paragraph_interval[paragraph_index] and paragraph_interval[paragraph_index] <= number_paragraph)
#         assert(0 < shot_interval[shot_index] and shot_interval[shot_index] <= number_shots)
        
        new_ground_truth.append({'Paragraph Number': paragraph_interval[paragraph_index], 
                                 'Shot Number': shot_interval[shot_index], 
                                 'type': alignment_type})
        
        # COMPARISON
        original_alignment_scores.append(text_features[:, alignment['id_paragraph']].T @ image_features[:, current_shot])
        new_alignment_scores.append(text_features[:, paragraph_interval[paragraph_index]].T @ image_features[:, shot_interval[shot_index]])
        
    plt.plot(original_alignment_scores)
    plt.plot(new_alignment_scores)
    plt.savefig('./{}/shot_paragraph_ground_truth_comparison.png'.format(book_name))
    
    np.save('./{}/shot_paragraph_ground_truth_mapping.npy'.format(book_name), new_ground_truth)
    
compute_ground_truth('American_Psycho')