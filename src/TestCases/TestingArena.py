import random

#=======================================Reappearance dependency maker======================================


# generating list with provided servers specifically to target them we can add more servers to increase more targtetted adversary attack using this code

# currently generatingf 256 
# Define the provided servers here
list_1 =  [5, 25, 71, 128, 141, 208, 270, 320, 342, 369, 375, 380, 387, 413, 518, 549, 601, 761, 844]
list_2 = [104, 466, 518, 540, 544, 585, 705, 712, 823]#94
list_3 = [140, 193, 198, 247, 287, 341, 501, 503, 594, 635, 714, 802, 816, 936, 949, 954, 995]
list_4 = [91, 137, 181, 316, 329, 403, 417, 420, 499, 546, 630, 691, 707, 813, 894]
list_5 = [135, 326, 464, 521, 549, 622, 728]#204
list_6 = [5, 25, 71, 128, 141, 208, 270, 320, 342, 369, 375, 380, 387, 413, 518, 549, 601, 761, 844]
list_7 = [131, 296, 413, 458, 765, 767, 820]#104
list_8 = [265, 352, 380, 465, 477, 586, 762, 789, 794, 994] #255
list_9 = [74, 143, 189, 463, 532, 591, 594, 654, 807, 836, 870, 953, 968]
list_10 = [3, 185, 295, 375, 381, 391, 452, 540, 685, 890]#55
list_10 =  [165, 183, 369, 384, 536, 539, 643, 747, 760, 874, 953] #110
list_11 = [197, 210, 258, 306, 354, 451, 453, 669, 796]
list_12 = [82, 238, 320, 368, 527, 724, 815, 852, 865, 876] #22
list_13 = [256, 327, 339, 374, 610, 612, 628, 731, 855, 892, 941, 967]
list_14 = [70, 116, 226, 282, 559, 708, 774, 866, 950, 957]
list_15 = [58, 208, 233, 304, 427, 443, 553, 702, 819] #9
list_16 = [5, 44, 64, 439, 493, 535, 686, 744, 752, 804, 911] #84
list_17 = [25, 81, 170, 283, 331, 341, 416, 512, 984] #178
list_18 = [43, 71, 119, 332, 568, 614, 816] #2
list_19 = [128, 337, 441, 564, 602, 615, 624, 749, 917, 925]#100
list_20 = [80, 130, 141, 196, 260, 746, 910] #160
list_21 = [549, 549, 549, 549, 549]
list_22 = [340, 567, 601, 753, 768, 835, 891, 945, 946, 952]
list_23 = [39, 262, 306, 501, 697, 761, 905]
list_24 = [325, 485, 597, 599, 680, 684, 844, 883]
list_25 = [238, 876, 815, 724]
list_26 = [342, 359, 462, 590, 921]
list_27 =  [539, 165, 384, 643] 


# Com20ne all the lists to ensure these numbers are 3ncluded
all_numbers = list_1 + list_2 + list_3 + list_4 + list_5 + list_7 + list_8 + list_9 + list_10 + list_11 + list_11 + list_12 + list_13 + list_14 + list_15 + list_16 + list_17 + list_18 + list_19 + list_20 +list_21 +list_22+list_23+list_24+list_25+list_26+list_27
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


print(final_list)