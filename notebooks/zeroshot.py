from typing import List
from sagemaker.huggingface import HuggingFaceModel
from tqdm import tqdm

BATCH_SIZE = 5


def zero_shot_classification_huggingface(
    sequence_to_classify: List, candidate_labels: List, instance_type: str, role: str
) -> list:
    """runs zero-shot classification on a list of sequences using a huggingface model on sagemaker"""

    # ensure the model knows it is a zero-shot model
    model_env = {
        "HF_TASK": "zero-shot-classification",
        "HF_MODEL_ID": "facebook/bart-large-mnli",
    }

    # create Hugging Face Model Class - will use existing model in SageMaker if model_name matches
    huggingface_model = HuggingFaceModel(
        role=role,
        transformers_version="4.6",
        pytorch_version="1.7",
        py_version="py36",
        env=model_env,
    )

    # create endpoint
    predictor = huggingface_model.deploy(
        initial_instance_count=1,
        instance_type=instance_type,
    )

    # batch

    output = []

    # capture a KeyboardInterrupt and delete the endpoint if triggered
    try:
        for i in tqdm(range(0, len(sequence_to_classify), BATCH_SIZE)):
            results = []
            for label in candidate_labels:
                data = {
                    "inputs": sequence_to_classify[i : i + BATCH_SIZE],
                    "parameters": {"candidate_labels": [label], "multi_label": True},
                }
                result = predictor.predict(data)
                if results:
                    for j, res in enumerate(result):
                        results[j]["scores"].extend(res["scores"])
                        results[j]["labels"].extend(res["labels"])
                else:
                    # if result is a list
                    if isinstance(result, list):
                        for res in result:
                            results.append(
                                {"scores": res["scores"], "labels": res["labels"]}
                            )
                    elif isinstance(result, dict):
                        results.append(
                            {"scores": result["scores"], "labels": result["labels"]}
                        )
                    else:
                        print(
                            "result must be a list or dict, but is {}".format(
                                type(result)
                            )
                        )

            output += results

        # kill endpoint
        predictor.delete_endpoint()
        return output

    except Exception as e:
        # kill endpoint if interrupted
        predictor.delete_endpoint()
        print("Error: ", e)
        print("Endpoint deleted")
        return output
