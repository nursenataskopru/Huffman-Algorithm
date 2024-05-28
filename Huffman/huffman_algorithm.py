from collections import Counter

class huffman_node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def huffman_tree(text):
    frq = Counter(text)
    nodes = [huffman_node(char, freq) for char, freq in frq.items()]

    while len(nodes) > 1:
        nodes.sort(key=lambda x: x.freq)
        left_node = nodes.pop(0)
        right_node = nodes.pop(0)

        l_r_nodes = huffman_node(None, left_node.freq + right_node.freq)
        l_r_nodes.left = left_node
        l_r_nodes.right = right_node

        nodes.append(l_r_nodes)

    root = nodes[0]

    print("Huffman Agaci (Preorder Sıralama):")
    print_huffman_tree(root)

    return root

def print_huffman_tree(node, depth=0):
    if node is not None:
        if node.char is not None:
            print("  " * depth + f"{node.char}: {node.freq}")
        else:
            print("  " * depth + f"[Ic Dugum]: {node.freq}")
        print_huffman_tree(node.left, depth + 1)
        print_huffman_tree(node.right, depth + 1)


def huffman_code(node, pre="", codes={}):
    if node is not None:
        if node.char is not None:
            codes[node.char] = pre
        huffman_code(node.left, pre + "0", codes)
        huffman_code(node.right, pre + "1", codes)
    return codes

def huffman_compressing(text, compressed_file):
    root = huffman_tree(text)
    codes = huffman_code(root)
    encoded_text = "".join(codes[char] for char in text)

    with open(compressed_file, 'w') as file:
        file.write(encoded_text)

    return codes, encoded_text

def build_huffman_tree(codes):
    root = huffman_node(None, None)
    for char, code in codes.items():
        node = root
        for bit in code:
            if bit == '0':
                if node.left is None:
                    node.left = huffman_node(None, None)
                node = node.left
            else:
                if node.right is None:
                    node.right = huffman_node(None, None)
                node = node.right
        node.char = char
    return root

def huffman_decompress(encoded_text, codes, output_file):
    root = build_huffman_tree(codes)
    current_node = root
    decoded_text = ""

    for i in encoded_text:
        if i == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_text += current_node.char
            current_node = root

    with open(output_file, 'w') as file:
        file.write(decoded_text)

input_file = "text.txt"
output_file = "compressed_output.txt"

with open(input_file, 'r') as file:
    text = file.read()

codes, encoded_text = huffman_compressing(text, output_file)
decoded_output_file = "decoded_text.txt"
huffman_decompress(encoded_text, codes, decoded_output_file)
