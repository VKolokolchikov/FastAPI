MAX_N = 9999
MIN_SUFFIX_BLOCK = 3 + len(str(MAX_N))


def get_len_suffix(array: list):
    lenght_array = len(array)

    if lenght_array < 10:
        return MIN_SUFFIX_BLOCK
    elif lenght_array < 100:
        return MIN_SUFFIX_BLOCK + 1
    elif lenght_array < 1000:
        return MIN_SUFFIX_BLOCK + 2
    elif lenght_array < 9999:
        return MIN_SUFFIX_BLOCK + 3

    raise Exception('!!!!')


def get_messages(
        string: str,
        max_length_sting: int = 100
):
    base_list = string.split(' ')
    result = []

    word = ''

    for item in base_list:
        if not word:
            word = item
            continue

        subword = word + (' ' + item)

        if len(subword) < (max_length_sting - get_len_suffix(result)):
            word = subword
        else:
            result.append(word)
            word = item

    max_message = len(result)

    for idx, item in enumerate(result, 0):
        result[idx] = item + f' {idx+1}/{max_message}'

    return result


string = "in iaculis nunc sed augue lacus viverra vitae congue eu consequat ac felis donec et odio pellentesque diam volutpat commodo sed egestas egestas fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien nec sagittis aliquam malesuada bibendum arcu vitae elementum curabitur vitae nunc sed velit dignissim sodales ut eu sem integer vitae justo eget magna fermentum iaculis eu non diam phasellus vestibulum lorem sed risus ultricies tristique nulla aliquet enim tortor at auctor urna nunc id cursus metus aliquam eleifend mi in nulla posuere sollicitudin aliquam ultrices sagittis orci a scelerisque purus semper eget duis at tellus at urna condimentum mattis pellentesque id nibh tortor id aliquet lectus proin nibh nisl condimentum id venenatis a condimentum vitae sapien pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas sed tempus urna et pharetra pharetra massa massa ultricies" * 700
res = get_messages(string)

for item in res:
    if len(item) > 100:
        print(item, len(item))
