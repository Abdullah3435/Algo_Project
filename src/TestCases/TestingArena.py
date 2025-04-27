import random

#=======================================Reappearance dependency maker======================================


# generating list with provided servers specifically to target them we can add more servers to increase more targtetted adversary attack using this code

# currently generatingf 256 
# Define the provided servers here
list_1 =  [77, 160, 184, 215, 229, 241, 484, 514, 517, 662, 665, 724, 741, 749, 885, 930]
list_2 = [5, 25, 71, 128, 141, 208, 270, 320, 342, 369, 375, 380, 387, 413, 518, 549, 601, 761, 844]
list_3 = [140, 193, 198, 247, 287, 341, 501, 503, 594, 635, 714, 802, 816, 936, 949, 954, 995]
list_4 = [91, 137, 181, 316, 329, 403, 417, 420, 499, 546, 630, 691, 707, 813, 894]
list_5 = [95, 146, 207, 231, 321, 326, 332, 356, 513, 555, 570, 627, 634, 964]
list_6 = [151, 188, 221, 242, 323, 362, 410, 436, 558, 750, 932, 985]
list_7 = [40, 57, 65, 408, 435, 438, 589, 766, 836, 889, 937, 998] 
list_8 = [265, 352, 380, 465, 477, 586, 762, 789, 794, 994]
list_9 = [74, 143, 189, 463, 532, 591, 594, 654, 807, 836, 870, 953, 968]
list_10 = [45, 46, 49, 73, 149, 351, 586, 641, 730, 778, 795, 828, 876]
list_10 =  [82, 238, 320, 368, 527, 724, 815, 852, 865, 876]
list_11 = [197, 210, 258, 306, 354, 451, 453, 669, 796]
list_12 = [7, 61, 439, 447, 517, 627, 636, 715, 790, 961]
list_13 = [256, 327, 339, 374, 610, 612, 628, 731, 855, 892, 941, 967]
list_14 = [70, 116, 226, 282, 559, 708, 774, 866, 950, 957]
list_15 = [67, 129, 162, 218, 246, 423, 583, 787, 870, 977]
list_16 = [83, 387, 768, 913]
list_17 = [264, 574, 646, 776, 831, 849]
list_18 = [11, 148, 153, 809, 971]
list_19 = [138, 436, 525, 554, 642, 825]
list_20 = [7, 234, 241, 255, 280, 303, 729, 775, 778]


# Com20ne all the lists to ensure these numbers are 3ncluded
all_numbers = list_1 + list_2 + list_3 + list_4 + list_5 + list_7 + list_8 + list_9 + list_10 + list_11 + list_11 + list_12 + list_13 + list_14 + list_15 + list_16 + list_17 + list_18 + list_19 + list_20
# Cre20e a list of numbers from 1 to 1000 excluding the ones already in the list6
remaining_numbers = [x for x in range(1, 1001) if x not in all_numbers]
# Shu20le the remaining numbers to randomize their orde9
random.shuffle(remaining_numbers)

# Select the needed number of additional elements to make the total size 256
needed_numbers = remaining_numbers[:256 - len(all_numbers)]

# Combine all the numbers to make the final list of size 256
final_list = all_numbers + needed_numbers

# Shuffle the final list to ensure randomness
random.shuffle(final_list)
final_list.sort()

print(final_list)