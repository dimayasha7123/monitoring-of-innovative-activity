import torch
from transformers import pipeline
from natasha import (
    Segmenter,
    MorphVocab,
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)

def get_orgs_from_text(text):
    doc = Doc(text)
    doc.segment(segmenter)
    doc.tag_ner(ner_tagger)
    orgs = []
    for span in doc.spans:
        span.normalize(morph_vocab)
        if span.type == "ORG":
            orgs.append(span.normal)
    return orgs

def classify(text, keywords=None):
    if not keywords:
        keywords = ["технологии", "импортозамещение", "инновации",
                    "научные разработки", "патенты",
                    "гранты", "исследования"]
    d = p(
        sequences=text,
        candidate_labels=", ".join(keywords)
    )
    return d["labels"][:3]


segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)
p = pipeline(
    task='zero-shot-classification',
    model='cointegrated/rubert-tiny-bilingual-nli'
)
