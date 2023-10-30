from itertools import groupby


def post_processing(labels):
    min_cluster_size = 3
    largest_sequences = get_largest_sequence(labels, min_cluster_size)
    merge_inner_cluster(largest_sequences, min_cluster_size, labels)
    split_inner_cluster(min_cluster_size, labels)
    fix_labels_order(labels)
    return labels


def split_inner_cluster(k, labels):
    i = 0
    while i < len(labels):
        curr_num = labels[i]
        curr_seq_len = 1
        # Find the length of the current sequence
        while i + 1 < len(labels) and labels[i + 1] == curr_num:
            curr_seq_len += 1
            i += 1
        if curr_seq_len < k or curr_num == -1:  # should remove noise
            prev_num_i = i - curr_seq_len
            next_num_i = i + 1
            first_half = []
            second_half = []
            # Split the sequence into two halves
            if prev_num_i < 0:
                second_half = [labels[next_num_i]] * curr_seq_len
            elif next_num_i >= len(labels):
                second_half = [labels[prev_num_i]] * curr_seq_len
            else:
                first_half = [labels[prev_num_i]] * (curr_seq_len // 2)
                second_half = [labels[next_num_i]] * (curr_seq_len // 2 + curr_seq_len % 2)
            labels[i - curr_seq_len + 1: i + 1] = first_half + second_half
            if next_num_i < len(labels):
                i = i - len(second_half)
        i += 1


def merge_inner_cluster(largest_sequences, min_cluster_size, labels):
    for l_seq_info in largest_sequences.items():
        seq_first_i = l_seq_info[1]['first_index']
        start_i = seq_first_i - min_cluster_size
        if start_i < 0:
            start_i = 0
        merge_cluster(start_i, seq_first_i, labels, l_seq_info[0])
        seq_last_i = l_seq_info[1]['last_index']
        end_i = seq_last_i + min_cluster_size
        if end_i > len(labels) - 1:
            end_i = len(labels) - 1
        merge_cluster(end_i, seq_last_i, labels, l_seq_info[0])


def merge_cluster(begin, end, labels, label):
    if begin > end:
        for i in range(begin, end, -1):
            if labels[i] == label:
                labels[end:i] = label
                return
    else:
        for i in range(begin, end):
            if labels[i] == label:
                labels[i:end + 1] = label
                return
    return


def fix_labels_order(arr):
    unique_nums = set(arr)
    highest_num = max(arr)
    while len(unique_nums) != highest_num + 1:
        for num in range(highest_num + 1):
            if num not in unique_nums:
                for j in range(len(arr)):
                    if arr[j] == highest_num:
                        arr[j] = num
        unique_nums = set(arr)
        highest_num = max(arr)
    return arr


def get_largest_sequence(arr, k):
    largest_sequences = {}
    # Iterate over grouped consecutive numbers
    for num, group in groupby(enumerate(arr), key=lambda x: x[1]):
        if num == -1:  # noise
            continue
        indices = [i for i, _ in group]  # Get the indices of the current group
        sequence_length = len(indices)

        if num not in largest_sequences:
            largest_sequences[num] = {
                'length': sequence_length,
                'first_index': indices[0],
                'last_index': indices[-1]
            }
        else:
            if sequence_length > largest_sequences[num]['length']:
                largest_sequences[num]['length'] = sequence_length
                largest_sequences[num]['first_index'] = indices[0]
                largest_sequences[num]['last_index'] = indices[-1]

    # Remove sequences with length smaller than k
    largest_sequences = {num: seq for num, seq in largest_sequences.items() if seq['length'] >= k}
    # Sort the result in descending order based on the lengths
    sorted_sequences = dict(sorted(largest_sequences.items(), key=lambda x: x[1]['length'], reverse=True))

    return sorted_sequences


def get_min_value(a, b):
    min_value = min(a, b)
    if min_value < 0:
        return 0
    return min_value
