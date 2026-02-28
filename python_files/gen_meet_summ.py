# from transformers import pipeline
# from python_files.clean_text import cleaned_text
#
# def gen_meet_summe(clean_texts):
#     summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
#
#     summary = summarizer(
#         cleaned_text,
#         max_length=150,
#         min_length=50,
#         do_sample=False
#     )
#     meeting_summary = summary[0]["summary_text"]
#     return meeting_summary
#
#
# summary = gen_meet_summe(cleaned_text)
# print(summary)


from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from python_files.clean_text import cleaned_text
import torch


def gen_meet_summe(clean_texts):
    # Load model and tokenizer directly
    model_name = "facebook/bart-large-cnn"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    # Tokenize the input text
    inputs = tokenizer(
        clean_texts,
        max_length=1024,
        truncation=True,
        return_tensors="pt"
    )

    # Generate summary
    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=150,
        min_length=50,
        do_sample=False,
        num_beams=4,
        early_stopping=True,
        no_repeat_ngram_size=3  # Prevents repetitive phrases
    )

    # Decode the summary
    meeting_summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return meeting_summary


# Call the function
# summary = gen_meet_summe(cleaned_text)
# print(summary)