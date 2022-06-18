import numpy as np
import scipy.io
import pdb

class Book:
    
    def __init__(self, book_name):
        self.book_name = book_name
        self.book = scipy.io.loadmat('../data/{}/book.mat'.format(book_name))['book']
        
    def get_word(self, sentence_id, word_id):
        num_words = int(self.book['sentences'].item()[sentence_id]['n_words'])
        if word_id >= num_words:
            return ''
        return self.book['sentences'].item()[sentence_id]['words'].item()[word_id].item()[0]
    
    def get_words(self, sentence_id):
        num_words = int(self.book['sentences'].item()[sentence_id]['n_words'])
        return [self.book['sentences'].item()[sentence_id]['words'].item()[word_id].item()[0] for word_id in range(num_words)]
    
    def get_sentence(self, sentence_id):
        return self.book['sentences'].item()[sentence_id]['sentence'][0].item()
    
    def get_sentences(self):
        num_sentences = int(self.book['sentences'].item().shape[0])
        return [self.book['sentences'].item()[sentence_id]['sentence'][0].item() for sentence_id in range(num_sentences)]
    
    def get_num_paragraphs(self):
        return self.book['paragraphs'].item().shape[1]
    
    def get_paragraph(self, paragraph_id):
        start_line = np.transpose(self.book['paragraphs'].item())[paragraph_id]['lines'].item()[0][0] - 1
        end_line = np.transpose(self.book['paragraphs'].item())[paragraph_id]['lines'].item()[0][1] - 1
        paragraph = ""
        for sentence_id in range(start_line, end_line + 1):
            paragraph += self.get_sentence(sentence_id)
        return paragraph
    
    def get_paragraphs(self):
        num_paragraphs = self.book['paragraphs'].item().shape[1]
        return [self.get_paragraph(paragraph_id) for paragraph_id in range(num_paragraphs)]
            
    def is_paragraph_dialogue(self, paragraph_id):
        dialogue_indicator = np.transpose(self.book['paragraphs'].item())[paragraph_id]['dialog'].item()[0]
        for i in dialogue_indicator:
            if i != 0: return True
        return False
    
    
# sample_book = Book('Harry_Potter_and_the_Sorcerers_Stone')
# print(sample_book.get_paragraphs()[0])
# print(sample_book.get_words(8))
# print(sample_book.get_sentence(3))
# print(sample_book.get_paragraph(3))
# print(sample_book.is_paragraph_dialogue(6))
# print(sample_book.get_sentences_paragraph(3))