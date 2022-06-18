import glob
import numpy as np
import clip_encoder
from parse_book import Book

def compute_clip_features(book_name):
    
    book = Book(book_name)
    sentences = book.get_sentences()
    text_features = np.array(clip_encoder.clip_text_encoder(sentences))
    np.save('./{}/sentence_features.npy'.format(book_name), text_features)
    
    frames_path = './{}/movie_scenes/*.jpg'.format(book_name)
    frames_files = sorted(glob.glob(frames_path))
    image_features = np.array(clip_encoder.clip_image_encoder(frames_files))
    np.save('./{}/shot_features.npy'.format(book_name), image_features)
    
def compute_paragraph_clip_features(book_name):
    book = Book(book_name)
    paragraphs = book.get_paragraphs()
    text_features = np.array(clip_encoder.clip_text_encoder(paragraphs))
    np.save('./{}/paragraph_features.npy'.format(book_name), text_features)
    
compute_paragraph_clip_features('American_Psycho')

