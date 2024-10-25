import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    def __init__(self, model_name, device, direction):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
        self.device = device
        self.direction = direction
        
    def translate_text(self, segments, max_length=512):
        translated_segments = []
        for segment in segments:
            text = segment['text'].strip()
            if text:
                # Split text into sentences using a simple regex
                sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
                translated_sentences = []
                for sentence in sentences:
                    inputs = self.tokenizer(sentence, return_tensors="pt", padding=True, truncation=True, max_length=max_length).input_ids.to(self.device)
                    outputs = self.model.generate(inputs)
                    translated_text = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
                    translated_sentences.append(translated_text[3:] if self.direction == "en_to_vn" else translated_text)
                translated_text = ' '.join(translated_sentences)
                translated_segments.append((segment['start'], segment['end'], translated_text))
        return translated_segments
        
    

