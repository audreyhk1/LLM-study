import torch
from secret import HUGGING_FACE_TOKEN
from huggingface_hub import login
from transformers import pipeline
login(token=HUGGING_FACE_TOKEN, add_to_git_credential=True)

"""
Running large datasets at one time
https://huggingface.co/docs/transformers/en/pipeline_tutorial#using-pipelines-on-a-dataset

Would rather use a pipeline (with a task) than have to fine-tune because fine-tuning requires to have to preprocess, train, evaluate, inference, etc
OR could potentially run inferences on pipeline directly
"""

# https://huggingface.co/docs/transformers/en/pipeline_tutorial#text-pipeline
# https://huggingface.co/docs/transformers/v4.44.0/en/main_classes/pipelines#transformers.pipeline
# https://huggingface.co/docs/transformers/v4.44.0/en/main_classes/pipelines#transformers.ZeroShotClassificationPipeline
#  This model is a `zero-shot-classification` model.
# It will classify text, except you are free to choose any label you might imagine
classifier = pipeline(model="facebook/bart-large-mnli")
results = classifier(
    "I have a problem with my iphone that needs to be resolved asap!!",
    candidate_labels=["urgent", "not urgent", "phone", "tablet", "computer"],
)
print(results)
