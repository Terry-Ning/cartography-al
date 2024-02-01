import torch

def pick_cases_iq(idx_with_probas, class_weights_pick, num):
    """
    Selects unique indices based on the predicted class and class weights.
    Each case is assigned to the class where it has the highest probability.

    Args:
    idx_with_probas (list of tuples): A list where each tuple contains an index and a list of probabilities.
    class_weights_pick (torch.FloatTensor): A tensor containing weights for each class.
    num (int): Total number of elements to select.

    Returns:
    list: A list of selected indices, ensuring each index is unique and selected based on its predicted class.
    """
    if not isinstance(num, int) or num <= 0:
        raise ValueError("num must be a positive integer")

    # # Assign predicted label based on highest probability and create a mapping
    # label_mapping = {idx: torch.argmax(torch.tensor(probas)).item() for idx, probas in idx_with_probas}
    # Assign predicted label based on highest probability and create a mapping
    label_mapping = {idx: torch.argmax(probas).item() for idx, probas in idx_with_probas}

    # Ensure total weight is not zero
    total_weight = torch.sum(torch.tensor(class_weights_pick))
    if total_weight == 0:
        raise ValueError("Total weight in class_weights_pick cannot be zero")

    # Normalize class weights and calculate the number of elements per class
    normalized_weights = class_weights_pick / total_weight
    num_per_group = [round(weight.item() * num) for weight in normalized_weights]


    # Adjust to ensure the total is exactly 'num'
    while sum(num_per_group) != num:
        difference = sum(num_per_group) - num
        for i in range(len(num_per_group)):
            if difference > 0 and num_per_group[i] > 0:
                num_per_group[i] -= 1
                difference -= 1
            elif difference < 0:
                num_per_group[i] += 1
                difference += 1
            if difference == 0:
                break

    selected_indices = []
    for grp_index, num_grp in enumerate(num_per_group):
        if num_grp != 0:
            # Filter indices for the current predicted class and sort by probability
            class_indices = [(idx, probas) for idx, probas in idx_with_probas if label_mapping[idx] == grp_index]
            class_indices.sort(key=lambda tup: tup[1][grp_index], reverse=True)

            a = len(selected_indices)
            # Select top indices based on sorted probabilities
            selected_indices.extend([idx for idx, _ in class_indices[:num_grp]])
            b= len(selected_indices)
            c = a-b

    return selected_indices


def pick_cases_iq_like_cal(idx_with_probas, num):
    idx_with_probas.sort(key=lambda tup: (torch.amax(tup[1])))
    top_k_indices = [idx.item() for idx, proba in idx_with_probas[:int(num)]]

    return top_k_indices
