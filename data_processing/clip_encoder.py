import torch
import clip
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from tqdm import tqdm

device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

class ImageDataset(Dataset):
    def __init__(self, image_files):
        self.image_files = image_files
     
    def __len__(self):
        return len(self.image_files)
   
    def __getitem__(self, idx):
        return preprocess(Image.open(self.image_files[idx]))
    
class TextDataset(Dataset):
    def __init__(self, sentences):
        self.sentences = sentences
        self.tokenized_sentences = clip.tokenize(self.sentences, truncate = True)

    def __len__(self):
        return len(self.sentences)

    def __getitem__(self, idx):
        return self.tokenized_sentences[idx]
    
def clip_image_encoder(files):
    dataset = ImageDataset(files)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False, sampler=None,
           batch_sampler=None, num_workers=30, collate_fn=None)
    image_features = []
    
    for i, batch in enumerate(tqdm(dataloader)):
        with torch.no_grad():
            image_features.append(model.encode_image(batch.to(device)))
    return torch.cat(image_features, axis=0).cpu()

def clip_text_encoder(sentences):
    dataset = TextDataset(sentences)
    dataloader = DataLoader(dataset, batch_size=64, shuffle=False, sampler=None,
           batch_sampler=None, num_workers=20, collate_fn=None)
    text_features = []
    for i, batch in enumerate(tqdm(dataloader)):
        with torch.no_grad():
            text_features.append(model.encode_text(batch.to(device)))
    return torch.cat(text_features, axis=0).cpu()
