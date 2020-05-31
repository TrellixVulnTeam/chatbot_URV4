import logging
import random
from itertools import chain
import warnings

import torch
import torch.nn.functional as F

from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizer
from server.botmgr.train import SPECIAL_TOKENS, build_input_from_segments, add_special_tokens_
from server.botmgr.utils import get_dataset

class ConversationalAiModel():

    def __init__(self, model_checkpoint: str, seed: int = 0):
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__file__)
        
        if seed != 0:
            random.seed(seed)
            torch.random.manual_seed(seed)


        logger.info("Get pretrained model and tokenizer")
        tokenizer_class, model_class = (OpenAIGPTTokenizer, OpenAIGPTLMHeadModel)
        self.tokenizer = tokenizer_class.from_pretrained(model_checkpoint)
        self.model = model_class.from_pretrained(model_checkpoint)
        self.model.to("cpu")
        add_special_tokens_(self.model, self.tokenizer)

        logger.info("Sample a personality")
        dataset = get_dataset(self.tokenizer, "", '/home/jsnouffer/git/transfer-learning-conv-ai/dataset_cache')
        personalities = [dialog["personality"] for dataset in dataset.values() for dialog in dataset]
        self.personality = random.choice(personalities)
        logger.info("Selected personality: %s", self.tokenizer.decode(chain(*self.personality)))

        self.history = []


    def top_filtering(self, logits, top_k=0., top_p=0.9, threshold=-float('Inf'), filter_value=-float('Inf')):
        """ Filter a distribution of logits using top-k, top-p (nucleus) and/or threshold filtering
            parameters:
                logits: logits distribution shape (vocabulary size)
                top_k: <=0: no filtering, >0: keep only top k tokens with highest probability.
                top_p: <=0.0: no filtering, >0.0: keep only a subset S of candidates, where S is the smallest subset
                    whose total probability mass is greater than or equal to the threshold top_p.
                    In practice, we select the highest probability tokens whose cumulative probability mass exceeds
                    the threshold top_p.
                threshold: a minimal threshold to keep logits
        """
        assert logits.dim() == 1  # Only work for batch size 1 for now - could update but it would obfuscate a bit the code
        top_k = min(top_k, logits.size(-1))
        if top_k > 0:
            # Remove all tokens with a probability less than the last token in the top-k tokens
            indices_to_remove = logits < torch.topk(logits, top_k)[0][..., -1, None]
            logits[indices_to_remove] = filter_value

        if top_p > 0.0:
            # Compute cumulative probabilities of sorted tokens
            sorted_logits, sorted_indices = torch.sort(logits, descending=True)
            cumulative_probabilities = torch.cumsum(F.softmax(sorted_logits, dim=-1), dim=-1)

            # Remove tokens with cumulative probability above the threshold
            sorted_indices_to_remove = cumulative_probabilities > top_p
            # Shift the indices to the right to keep also the first token above the threshold
            sorted_indices_to_remove[..., 1:] = sorted_indices_to_remove[..., :-1].clone()
            sorted_indices_to_remove[..., 0] = 0

            # Back to unsorted indices and set them to -infinity
            indices_to_remove = sorted_indices[sorted_indices_to_remove]
            logits[indices_to_remove] = filter_value

        indices_to_remove = logits < threshold
        logits[indices_to_remove] = filter_value

        return logits


    def sample_sequence(self, current_output=None):
        special_tokens_ids = self.tokenizer.convert_tokens_to_ids(SPECIAL_TOKENS)
        if current_output is None:
            current_output = []

        for i in range(20):
            instance = build_input_from_segments(self.personality, self.history, current_output, self.tokenizer, with_eos=False)

            input_ids = torch.tensor(instance["input_ids"], device="cpu").unsqueeze(0)
            token_type_ids = torch.tensor(instance["token_type_ids"], device="cpu").unsqueeze(0)

            logits = self.model(input_ids, token_type_ids=token_type_ids)
            if isinstance(logits, tuple):  # for gpt2 and maybe others
                logits = logits[0]
            logits = logits[0, -1, :] / 0.7
            logits = self.top_filtering(logits, top_k=0.0, top_p=0.9)
            probs = F.softmax(logits, dim=-1)

            prev = torch.multinomial(probs, 1)
            if i < 1 and prev.item() in special_tokens_ids:
                while prev.item() in special_tokens_ids:
                    if probs.max().item() == 1:
                        warnings.warn("Warning: model generating special token with probability 1.")
                        break  # avoid infinitely looping over special token
                    prev = torch.multinomial(probs, num_samples=1)

            if prev.item() in special_tokens_ids:
                break
            current_output.append(prev.item())

        return current_output

    def process(self, raw_text: str):
        self.history.append(self.tokenizer.encode(raw_text))
        with torch.no_grad():
            out_ids = self.sample_sequence()
        
        self.history.append(out_ids)
        max_history: int = 2
        self.history = self.history[-(2*max_history+1):]
        
        return self.tokenizer.decode(out_ids, skip_special_tokens=True)
