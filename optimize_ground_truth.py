import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
 
FRAME_NEIGHBORHOOD = 10
SENTENCE_NEIGHBORHOOD = 10

def timestamp_to_seconds(timestamp):
    [hours, minutes, seconds] = timestamp.split(':')
    return 3600 * float(hours) + 60 * float(minutes) + float(seconds)

def compute_ground_truth(book_name):
    
    original_ground_truth = json.load(open(f'./{book_name}/ground_truth_annotation.json'))
    
    image_features = np.asarray(np.load(f'./{book_name}/frame_features.npy').T, dtype = np.float64)
    image_features /= np.linalg.norm(image_features, axis=0, keepdims=True)
    
    text_features = np.asarray(np.load(f'./{book_name}/sentence_features.npy').T, dtype = np.float64)
    text_features /= np.linalg.norm(text_features, axis=0, keepdims=True)
    
    number_frames = image_features.shape[1]
    number_sentences = text_features.shape[1]
    
    new_ground_truth = []
    original_alignment_scores = []
    new_alignment_scores = []
    
    for alignment in original_ground_truth:
        [start_frame_timestamp, end_frame_timestamp] = alignment['Time Shot'].split(' ')
        start_frame = int(timestamp_to_seconds(start_frame_timestamp)) * 2
        end_frame = int(timestamp_to_seconds(end_frame_timestamp)) * 2
        mid_frame = int((start_frame + end_frame) / 2)
        
        frame_interval_start = max(0, mid_frame - FRAME_NEIGHBORHOOD)
        frame_interval_end = min(number_frames, mid_frame + FRAME_NEIGHBORHOOD)
        frame_interval = np.array([frame for frame in range(frame_interval_start, frame_interval_end)])
        
        sentence_interval_start = max(0, alignment['id_sentence'] - SENTENCE_NEIGHBORHOOD)
        sentence_interval_end = min(number_sentences, alignment['id_sentence'] + SENTENCE_NEIGHBORHOOD)
        sentence_interval = np.array([sentence for sentence in range(sentence_interval_start, sentence_interval_end)])
        
        matrix = text_features[:, sentence_interval].T @ image_features[:, frame_interval]
        # (20, 512) x (512, 20) = (20, 20)
        
        matrix_coordinates = np.unravel_index(np.argsort(matrix, axis=None)[::-1], matrix.shape)
        
        sentence_index = matrix_coordinates[0][0]
        frame_index = matrix_coordinates[1][0]
        alignment_type = [int('Dialog' in alignment['Alignment Type']), int('Visual' in alignment['Alignment Type']), int('Sound' in alignment['Alignment Type'])]
        
#         assert(0 < sentence_interval[sentence_index] and sentence_interval[sentence_index] <= number_sentences)
        assert(0 < frame_interval[frame_index] and frame_interval[frame_index] <= number_frames)
        
        new_ground_truth.append({'Sentence Number': sentence_interval[sentence_index], 
                                 'Frame Number': frame_interval[frame_index], 
                                 'type': alignment_type})
        
        # COMPARISON
        original_alignment_scores.append(text_features[:, alignment['id_sentence']].T @ image_features[:, mid_frame])
        new_alignment_scores.append(text_features[:, sentence_interval[sentence_index]].T @ image_features[:, frame_interval[frame_index]])
        
    plt.plot(original_alignment_scores)
    plt.plot(new_alignment_scores)
    plt.savefig(f'./{book_name}/frame_sentence_ground_truth_comparison.png')
        
    np.save(f'./{book_name}/frame_sentence_ground_truth_mapping.npy', new_ground_truth)
    
compute_ground_truth('The_Shawshank_Redemption')
