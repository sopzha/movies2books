import json
import matplotlib.pyplot as plt
import numpy as np

def time_to_seconds(time):
    hours, minutes, seconds = time.split(':')
    return 3600 * int(hours) + 60 * int(minutes) + float(seconds)

def visualize_alignments(book_name):
    with open('./{}/alignments.json'.format(book_name), 'r') as f:
        alignments = json.load(f)

    num_seconds_movie = alignments[0]['movie_stats']['n_seconds']
    num_sentences_book = alignments[0]['movie_stats']['n_sentences']
    num_paragraphs_book = alignments[0]['movie_stats']['n_paragraphs']

    movie_time_alignments = np.array([time_to_seconds(shot['Time Clip']) for shot in alignments]) / num_seconds_movie
    book_sentence_alignments = np.array([shot['id_sentence'] for shot in alignments])/num_sentences_book
    book_paragraph_alignments = np.array([shot['id_paragraph'] for shot in alignments])/num_paragraphs_book
    
    plt.figure(figsize = (20, 5))
    
    plt.subplot(211)
    plt.title('Book Sentence to Movie Time Alignments')
    plt.axis('off')
    plt.scatter(book_sentence_alignments, np.ones(len(book_sentence_alignments)))
    plt.scatter(book_paragraph_alignments, np.zeros(len(movie_time_alignments)))
    for shot in alignments:
        if shot['Alignment Type'] == 'Dialog':
            plt.plot([time_to_seconds(shot['Time Clip'])/num_seconds_movie, shot['id_sentence']/num_sentences_book], [0, 1], color='m')
        else:
            plt.plot([time_to_seconds(shot['Time Clip'])/num_seconds_movie, shot['id_sentence']/num_sentences_book], [0, 1], color='g')
    
    plt.subplot(212)
    plt.title('Book Paragraph to Movie Time Alignments')
    plt.axis('off')
    plt.scatter(book_paragraph_alignments, np.ones(len(book_paragraph_alignments)))
    plt.scatter(movie_time_alignments, np.zeros(len(movie_time_alignments)))
    for shot in alignments:
        if shot['Alignment Type'] == 'Dialog':
            plt.plot([time_to_seconds(shot['Time Clip'])/num_seconds_movie, shot['id_paragraph']/num_paragraphs_book], [0, 1], color='m')
        else:
            plt.plot([time_to_seconds(shot['Time Clip'])/num_seconds_movie, shot['id_paragraph']/num_paragraphs_book], [0, 1], color='g')
            
    plt.savefig('./{}/alignments.png'.format(book_name))

visualize_alignments('Brokeback_Mountain')