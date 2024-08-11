"""
question-answering
"""
import torch
from secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)

# from transformers import pipeline

# # used HuggingChat 
# qa_pipeline = pipeline("question-answering", model="distilbert-base-uncased")
# question = "What is the capital of France?"
# context = "Paris London Berlin Rome"
# result = qa_pipeline(question = question, context = context)

# print("here", result)

"""
multiple choice
"""
# from transformers import AutoTokenizer


# prompt = "France has a bread law, Le Décret Pain, with strict rules on what is allowed in a traditional baguette."
# candidate1 = "The law does not apply to croissants and brioche."
# candidate2 = "The law applies to baguettes."

# tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
# inputs = tokenizer([[prompt, candidate1], [prompt, candidate2]], return_tensors="pt", padding=True)
# labels = torch.tensor(0).unsqueeze(0)

# from transformers import AutoModelForMultipleChoice

# model = AutoModelForMultipleChoice.from_pretrained("bert-base-uncased")
# outputs = model(**{k: v.unsqueeze(0) for k, v in inputs.items()}, labels=labels)
# logits = outputs.logits

# predicted_class = logits.argmax().item()

"""
text-generation
"""


"""
Running large datasets at one time
https://huggingface.co/docs/transformers/en/pipeline_tutorial#using-pipelines-on-a-dataset

Would rather use a pipeline (with a task) than have to fine-tune because fine-tuning requires to have to preprocess, train, evaluate, inference, etc
OR could potentially run inferences on pipeline directly
"""