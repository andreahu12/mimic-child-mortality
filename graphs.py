import json
from collections import Counter
import datetime

import matplotlib.ticker as plticker
import matplotlib.pyplot as plt
plt.rcdefaults()
import matplotlib.mlab as mlab
from sets import Set
import csv
import numpy as np
from matplotlib import pyplot
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import rcParams
from matplotlib.figure import Figure
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter, MaxNLocator

import csv
import pandas as pd
import numpy as np
from tfidf import tf_idf
import enchant
import string

def load_data():

    # notes per patient
    # x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 257, 258, 259, 260, 262, 263, 264, 265, 266, 268, 269, 270, 272, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 292, 293, 295, 296, 297, 298, 299, 300, 301, 302, 303, 305, 306, 308, 309, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 324, 325, 327, 329, 330, 331, 332, 333, 334, 335, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 350, 351, 352, 353, 355, 356, 357, 359, 360, 361, 362, 363, 364, 365, 366, 368, 369, 370, 372, 374, 375, 377, 378, 379, 380, 382, 383, 384, 385, 389, 390, 393, 394, 395, 396, 398, 399, 400, 402, 403, 404, 405, 406, 408, 412, 413, 414, 416, 419, 422, 423, 425, 426, 427, 429, 432, 433, 434, 435, 439, 441, 442, 443, 444, 448, 449, 451, 455, 458, 462, 463, 464, 465, 466, 469, 471, 476, 477, 482, 484, 486, 493, 494, 495, 496, 499, 508, 514, 516, 521, 527, 529, 531, 536, 537, 538, 539, 540, 544, 545, 549, 550, 553, 554, 555, 556, 557, 561, 564, 567, 571, 575, 576, 582, 586, 592, 593, 594, 595, 596, 598, 600, 604, 609, 613, 618, 620, 626, 627, 635, 641, 643, 649, 650, 651, 654, 655, 663, 669, 672, 673, 674, 681, 691, 693, 698, 699, 704, 708, 710, 713, 717, 726, 740, 743, 744, 746, 752, 765, 766, 786, 787, 788, 800, 806, 814, 816, 821, 825, 831, 837, 848, 865, 868, 888, 892, 916, 920, 941, 944, 980, 1004, 1059, 1076]
    # y = [172, 173, 157, 167, 125, 115, 82, 80, 73, 67, 53, 38, 53, 45, 42, 30, 35, 38, 31, 31, 38, 31, 31, 44, 39, 41, 35, 37, 34, 35, 29, 38, 40, 40, 34, 32, 29, 33, 29, 33, 32, 22, 24, 25, 24, 29, 24, 23, 28, 23, 17, 23, 18, 27, 27, 17, 15, 27, 18, 14, 15, 24, 20, 15, 15, 17, 27, 17, 25, 13, 22, 12, 14, 14, 15, 22, 12, 19, 16, 14, 16, 11, 13, 20, 7, 6, 12, 10, 14, 14, 13, 9, 12, 16, 11, 7, 8, 7, 12, 12, 9, 5, 11, 8, 4, 6, 5, 4, 7, 5, 14, 12, 9, 8, 3, 9, 5, 7, 4, 7, 11, 7, 4, 5, 7, 5, 4, 7, 3, 6, 9, 1, 8, 4, 4, 7, 2, 2, 7, 3, 3, 8, 8, 7, 2, 2, 5, 7, 6, 4, 5, 5, 4, 4, 4, 6, 4, 1, 4, 3, 8, 5, 3, 8, 3, 4, 4, 2, 8, 4, 7, 5, 6, 4, 5, 5, 3, 2, 3, 8, 3, 5, 4, 7, 1, 4, 3, 4, 10, 4, 4, 3, 4, 5, 5, 4, 4, 3, 5, 5, 1, 4, 4, 4, 4, 3, 3, 4, 3, 1, 7, 1, 4, 3, 3, 6, 3, 1, 2, 6, 4, 3, 2, 5, 1, 6, 1, 3, 1, 3, 2, 2, 4, 2, 1, 5, 2, 3, 3, 4, 2, 4, 3, 2, 3, 1, 3, 1, 2, 2, 3, 1, 4, 3, 6, 1, 3, 2, 3, 4, 6, 1, 1, 3, 4, 4, 2, 2, 4, 2, 2, 1, 1, 3, 2, 3, 2, 2, 1, 2, 3, 1, 2, 2, 4, 6, 1, 3, 2, 2, 2, 3, 1, 3, 3, 3, 2, 1, 2, 2, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 2, 2, 1, 2, 1, 1, 2, 1, 2, 3, 2, 1, 1, 1, 2, 1, 1, 1, 3, 1, 2, 1, 2, 1, 1, 2, 1, 4, 1, 1, 4, 1, 2, 1, 1, 1, 1, 4, 1, 1, 3, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 3, 1, 1, 1, 4, 1, 1, 1, 1, 1, 4, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 4, 1, 1, 1, 2, 2, 2, 2, 2, 1, 3, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1]

    # words per note
    # x =  [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 157, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240, 241, 242, 243, 244, 245, 246, 247, 248, 249, 250, 251, 252, 253, 254, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 299, 300, 301, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 360, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 414, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 441, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 452, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 476, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500, 501, 502, 503, 504, 505, 506, 507, 508, 509, 510, 511, 512, 513, 514, 515, 516, 517, 518, 519, 520, 521, 522, 523, 524, 525, 526, 527, 528, 529, 530, 531, 532, 533, 534, 535, 536, 537, 538, 539, 540, 541, 542, 544, 545, 546, 547, 548, 549, 550, 551, 552, 553, 555, 556, 557, 558, 559, 560, 561, 562, 563, 564, 565, 566, 567, 568, 569, 570, 571, 572, 573, 574, 575, 576, 577, 578, 579, 580, 581, 582, 583, 584, 585, 586, 587, 588, 589, 590, 591, 592, 593, 594, 595, 596, 597, 598, 599, 600, 601, 602, 603, 604, 605, 606, 607, 608, 609, 610, 611, 612, 613, 614, 615, 616, 617, 618, 619, 620, 621, 622, 623, 624, 625, 626, 627, 628, 629, 630, 631, 632, 633, 634, 635, 636, 637, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 650, 651, 652, 653, 654, 655, 656, 657, 658, 659, 660, 661, 662, 663, 664, 665, 666, 667, 668, 669, 670, 671, 672, 673, 674, 675, 676, 677, 678, 679, 680, 681, 682, 683, 684, 685, 686, 687, 688, 689, 690, 691, 692, 693, 694, 695, 696, 697, 698, 699, 700, 701, 702, 703, 704, 705, 706, 707, 708, 709, 710, 711, 712, 713, 714, 715, 716, 717, 718, 719, 720, 721, 722, 723, 724, 725, 726, 727, 728, 729, 730, 731, 732, 733, 734, 735, 736, 737, 738, 739, 740, 741, 742, 743, 744, 745, 746, 747, 748, 749, 750, 751, 752, 753, 754, 755, 756, 757, 758, 759, 760, 761, 762, 763, 764, 765, 766, 767, 768, 769, 770, 771, 772, 773, 774, 775, 776, 777, 778, 779, 780, 781, 782, 783, 784, 785, 786, 787, 788, 789, 790, 791, 792, 793, 794, 795, 796, 797, 798, 799, 800, 801, 802, 803, 804, 805, 806, 807, 808, 809, 810, 811, 812, 813, 814, 815, 816, 817, 818, 819, 820, 821, 822, 823, 824, 825, 826, 827, 828, 829, 830, 831, 832, 833, 834, 835, 836, 837, 838, 839, 840, 841, 842, 843, 844, 845, 846, 847, 848, 849, 850, 851, 852, 853, 854, 855, 856, 857, 858, 859, 860, 861, 862, 863, 864, 865, 866, 867, 868, 869, 870, 871, 872, 873, 874, 875, 876, 877, 878, 879, 880, 881, 882, 883, 884, 885, 886, 887, 888, 889, 890, 891, 892, 893, 894, 895, 896, 897, 898, 899, 900, 901, 902, 903, 904, 905, 906, 907, 908, 909, 910, 911, 912, 913, 914, 915, 916, 917, 918, 919, 920, 921, 922, 923, 924, 925, 926, 927, 928, 929, 930, 931, 932, 933, 934, 935, 936, 937, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 950, 951, 952, 953, 954, 955, 956, 957, 958, 959, 960, 961, 962, 963, 964, 965, 966, 967, 968, 969, 970, 971, 972, 973, 974, 975, 976, 977, 978, 979, 980, 981, 982, 983, 984, 985, 986, 987, 988, 989, 990, 991, 992, 993, 994, 995, 996, 997, 998, 999, 1000, 1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 1013, 1014, 1015, 1016, 1017, 1018, 1019, 1020, 1021, 1022, 1023, 1024, 1025, 1026, 1027, 1028, 1029, 1030, 1031, 1032, 1033, 1034, 1035, 1036, 1037, 1038, 1039, 1040, 1041, 1042, 1043, 1044, 1045, 1046, 1047, 1048, 1049, 1050, 1051, 1052, 1053, 1054, 1055, 1056, 1057, 1058, 1059, 1060, 1061, 1062, 1063, 1064, 1065, 1066, 1067, 1068, 1069, 1070, 1071, 1072, 1073, 1074, 1075, 1076, 1077, 1078, 1079, 1080, 1082, 1083, 1084, 1085, 1086, 1087, 1088, 1089, 1090, 1091, 1092, 1093, 1094, 1095, 1096, 1097, 1098, 1099, 1100, 1101, 1102, 1103, 1104, 1105, 1106, 1107, 1108, 1109, 1110, 1111, 1112, 1113, 1114, 1115, 1116, 1117, 1118, 1120, 1121, 1123, 1124, 1125, 1126, 1127, 1128, 1129, 1130, 1132, 1133, 1134, 1135, 1136, 1137, 1138, 1139, 1140, 1141, 1142, 1143, 1144, 1145, 1146, 1147, 1148, 1149, 1150, 1151, 1152, 1153, 1154, 1155, 1156, 1157, 1158, 1159, 1160, 1161, 1162, 1163, 1164, 1165, 1166, 1167, 1168, 1169, 1170, 1171, 1172, 1173, 1174, 1175, 1176, 1177, 1178, 1179, 1181, 1182, 1183, 1184, 1185, 1186, 1187, 1188, 1189, 1190, 1191, 1192, 1193, 1194, 1195, 1196, 1197, 1198, 1199, 1200, 1201, 1202, 1203, 1204, 1205, 1206, 1207, 1208, 1209, 1211, 1212, 1213, 1214, 1215, 1216, 1217, 1219, 1220, 1221, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1232, 1233, 1234, 1235, 1236, 1237, 1238, 1239, 1241, 1244, 1245, 1246, 1247, 1249, 1251, 1254, 1255, 1256, 1257, 1259, 1260, 1261, 1263, 1264, 1266, 1267, 1268, 1269, 1270, 1271, 1272, 1273, 1275, 1276, 1277, 1278, 1280, 1281, 1283, 1284, 1285, 1286, 1287, 1288, 1289, 1291, 1292, 1293, 1294, 1295, 1296, 1297, 1298, 1300, 1301, 1302, 1304, 1306, 1308, 1309, 1310, 1311, 1312, 1313, 1314, 1316, 1317, 1318, 1321, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1330, 1331, 1332, 1333, 1334, 1336, 1338, 1340, 1342, 1343, 1344, 1345, 1346, 1349, 1350, 1351, 1352, 1353, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1366, 1367, 1368, 1369, 1370, 1371, 1374, 1375, 1377, 1378, 1379, 1383, 1384, 1385, 1389, 1390, 1391, 1393, 1394, 1396, 1397, 1398, 1399, 1400, 1401, 1403, 1404, 1405, 1406, 1407, 1408, 1409, 1411, 1412, 1413, 1414, 1415, 1416, 1417, 1418, 1419, 1420, 1421, 1427, 1431, 1432, 1436, 1437, 1438, 1439, 1440, 1441, 1443, 1444, 1445, 1446, 1448, 1453, 1454, 1455, 1456, 1457, 1459, 1460, 1461, 1463, 1465, 1467, 1468, 1469, 1470, 1473, 1474, 1476, 1477, 1479, 1481, 1482, 1483, 1485, 1486, 1487, 1489, 1491, 1492, 1494, 1495, 1497, 1498, 1499, 1502, 1503, 1504, 1505, 1508, 1510, 1511, 1512, 1513, 1517, 1519, 1521, 1522, 1523, 1524, 1526, 1527, 1528, 1530, 1532, 1533, 1536, 1538, 1539, 1540, 1544, 1545, 1550, 1551, 1552, 1554, 1555, 1556, 1557, 1559, 1566, 1568, 1573, 1574, 1575, 1576, 1577, 1580, 1585, 1586, 1590, 1592, 1599, 1602, 1610, 1613, 1614, 1615, 1616, 1618, 1619, 1624, 1625, 1627, 1628, 1629, 1631, 1632, 1634, 1635, 1638, 1641, 1642, 1644, 1645, 1652, 1654, 1655, 1661, 1665, 1672, 1673, 1674, 1679, 1680, 1683, 1686, 1690, 1693, 1694, 1704, 1705, 1714, 1717, 1718, 1720, 1721, 1722, 1727, 1728, 1731, 1738, 1739, 1740, 1741, 1743, 1745, 1746, 1749, 1755, 1757, 1758, 1764, 1768, 1769, 1770, 1772, 1774, 1775, 1782, 1784, 1786, 1789, 1791, 1793, 1802, 1805, 1810, 1811, 1821, 1822, 1825, 1834, 1844, 1848, 1850, 1852, 1853, 1854, 1856, 1857, 1858, 1860, 1862, 1864, 1866, 1868, 1872, 1873, 1875, 1876, 1877, 1883, 1885, 1886, 1890, 1899, 1900, 1902, 1906, 1912, 1913, 1917, 1921, 1926, 1928, 1945, 1946, 1947, 1958, 1972, 1979, 1992, 1996, 1999, 2008, 2012, 2013, 2017, 2018, 2024, 2029, 2036, 2047, 2049, 2050, 2053, 2060, 2068, 2079, 2081, 2082, 2084, 2099, 2101, 2102, 2118, 2127, 2145, 2154, 2165, 2168, 2174, 2175, 2179, 2190, 2192, 2201, 2217, 2229, 2232, 2251, 2273, 2277, 2284, 2289, 2296, 2299, 2306, 2323, 2325, 2332, 2362, 2389, 2405, 2419, 2421, 2432, 2437, 2442, 2451, 2463, 2503, 2512, 2630, 2645, 2693, 2780, 3064, 3085, 3127]
    # y =  [4, 9, 18, 80, 253, 300, 432, 653, 1648, 907, 1101, 1695, 1187, 1115, 1488, 1161, 1128, 1396, 1470, 1537, 1574, 1761, 1842, 1914, 2025, 2269, 2288, 2564, 2523, 2601, 2674, 2635, 2865, 2776, 3014, 3101, 3117, 3206, 3197, 3320, 3467, 3096, 2995, 3291, 2979, 3143, 2839, 2881, 2818, 2845, 2656, 2744, 2672, 2704, 2567, 2575, 2527, 2599, 2587, 2494, 2359, 2469, 2370, 2444, 2388, 2352, 2396, 2424, 2346, 2333, 2318, 2350, 2337, 2240, 2270, 2201, 2135, 2121, 2244, 2139, 2208, 2152, 2174, 2150, 2261, 2122, 2088, 2084, 2095, 2068, 2029, 2062, 2092, 1973, 2008, 1930, 1989, 1905, 1908, 1903, 1834, 1876, 1795, 1837, 1867, 1777, 1764, 1779, 1744, 1784, 1747, 1747, 1853, 1730, 1795, 1726, 1710, 1807, 1745, 1699, 1792, 1681, 1726, 1690, 1780, 1664, 1726, 1644, 1716, 1649, 1686, 1751, 1620, 1696, 1696, 1613, 1657, 1672, 1601, 1614, 1561, 1591, 1546, 1627, 1523, 1541, 1427, 1459, 1482, 1501, 1442, 1413, 1473, 1403, 1353, 1315, 1358, 1355, 1390, 1302, 1331, 1346, 1242, 1227, 1232, 1276, 1198, 1198, 1156, 1186, 1153, 1165, 1143, 1146, 1107, 1154, 1032, 1117, 1044, 1060, 1003, 1033, 993, 972, 909, 965, 950, 923, 898, 872, 847, 864, 838, 829, 796, 828, 832, 783, 722, 768, 778, 699, 737, 716, 721, 692, 633, 698, 631, 644, 665, 593, 605, 578, 602, 565, 551, 574, 549, 511, 533, 508, 476, 520, 498, 492, 446, 425, 428, 470, 438, 432, 421, 439, 390, 412, 371, 370, 350, 376, 383, 356, 356, 284, 320, 316, 315, 337, 308, 291, 279, 295, 308, 299, 268, 280, 266, 260, 227, 250, 234, 248, 249, 271, 212, 224, 201, 222, 243, 216, 180, 195, 170, 169, 176, 184, 192, 192, 155, 184, 174, 191, 180, 171, 158, 143, 149, 146, 151, 125, 146, 130, 145, 116, 141, 123, 146, 135, 137, 144, 133, 133, 124, 126, 111, 120, 112, 103, 110, 97, 122, 129, 114, 105, 86, 120, 93, 99, 87, 118, 115, 108, 92, 84, 107, 104, 102, 93, 83, 109, 109, 101, 98, 82, 92, 96, 87, 81, 96, 90, 76, 94, 80, 78, 78, 76, 73, 80, 55, 69, 65, 67, 50, 59, 52, 44, 53, 45, 51, 37, 43, 41, 32, 44, 38, 31, 34, 22, 26, 21, 22, 36, 27, 19, 18, 17, 15, 16, 25, 12, 15, 18, 26, 18, 12, 14, 11, 14, 9, 10, 14, 10, 11, 9, 6, 8, 12, 7, 6, 10, 12, 7, 6, 6, 5, 4, 2, 6, 3, 6, 7, 11, 5, 10, 8, 3, 4, 6, 3, 5, 4, 5, 4, 4, 5, 6, 4, 10, 5, 7, 6, 6, 1, 5, 6, 7, 3, 6, 1, 5, 6, 4, 3, 3, 5, 8, 6, 4, 4, 4, 6, 5, 3, 6, 5, 2, 2, 3, 8, 6, 1, 3, 6, 5, 3, 7, 4, 4, 6, 5, 1, 7, 2, 3, 6, 2, 5, 2, 4, 2, 5, 5, 1, 9, 2, 1, 3, 7, 3, 2, 1, 3, 3, 9, 2, 4, 3, 3, 6, 4, 8, 2, 1, 3, 1, 4, 3, 4, 2, 2, 3, 5, 8, 1, 3, 5, 3, 3, 2, 4, 2, 5, 9, 4, 3, 4, 1, 5, 7, 4, 4, 5, 7, 6, 2, 6, 5, 1, 7, 3, 7, 2, 2, 4, 3, 5, 1, 4, 4, 5, 4, 1, 2, 6, 4, 4, 2, 3, 3, 2, 1, 1, 5, 4, 1, 5, 4, 3, 4, 3, 2, 3, 3, 5, 9, 3, 4, 5, 4, 4, 4, 4, 1, 4, 6, 4, 1, 2, 2, 3, 3, 1, 3, 4, 1, 3, 4, 3, 4, 1, 4, 5, 1, 4, 3, 2, 3, 3, 7, 4, 3, 3, 1, 2, 3, 2, 3, 4, 3, 3, 2, 4, 5, 3, 6, 2, 3, 4, 4, 8, 2, 4, 2, 5, 2, 3, 6, 3, 3, 3, 3, 5, 1, 8, 3, 3, 3, 3, 5, 6, 2, 4, 2, 4, 4, 4, 7, 4, 1, 7, 4, 1, 9, 4, 2, 3, 1, 1, 6, 5, 2, 8, 3, 3, 3, 1, 6, 3, 5, 4, 1, 3, 6, 4, 4, 5, 4, 1, 2, 8, 3, 3, 4, 8, 3, 5, 4, 6, 4, 9, 5, 5, 2, 6, 6, 3, 3, 6, 6, 4, 6, 7, 4, 3, 4, 3, 5, 5, 5, 7, 4, 7, 7, 5, 3, 2, 7, 5, 8, 4, 6, 4, 4, 3, 5, 8, 4, 6, 2, 6, 2, 5, 4, 5, 5, 4, 5, 3, 6, 2, 7, 8, 4, 2, 5, 5, 4, 3, 3, 9, 4, 10, 2, 2, 7, 5, 3, 2, 9, 5, 3, 4, 6, 7, 5, 3, 3, 2, 6, 4, 5, 5, 8, 9, 5, 2, 2, 1, 4, 5, 11, 3, 1, 5, 6, 5, 5, 1, 7, 3, 4, 4, 7, 6, 4, 2, 6, 4, 6, 2, 5, 8, 5, 3, 4, 8, 6, 5, 4, 7, 2, 4, 6, 5, 6, 5, 5, 3, 5, 3, 7, 6, 5, 4, 3, 4, 5, 8, 4, 3, 5, 5, 8, 4, 12, 2, 1, 8, 4, 6, 5, 4, 4, 2, 6, 7, 8, 3, 3, 7, 7, 3, 3, 4, 6, 1, 2, 5, 4, 5, 10, 6, 7, 4, 7, 4, 5, 5, 4, 5, 2, 3, 4, 5, 2, 3, 4, 8, 5, 6, 3, 4, 7, 6, 4, 7, 6, 3, 7, 3, 6, 4, 8, 6, 6, 6, 4, 7, 6, 6, 7, 8, 5, 4, 4, 9, 7, 5, 6, 8, 7, 3, 2, 2, 4, 5, 4, 6, 5, 4, 6, 5, 7, 6, 5, 7, 3, 6, 6, 7, 4, 4, 6, 5, 4, 7, 7, 6, 6, 7, 5, 3, 4, 6, 6, 5, 1, 1, 5, 3, 5, 4, 7, 4, 3, 7, 3, 6, 3, 3, 1, 4, 4, 6, 7, 4, 5, 4, 6, 3, 5, 6, 3, 5, 4, 4, 3, 3, 4, 3, 5, 5, 9, 12, 4, 5, 6, 6, 2, 5, 1, 7, 5, 3, 5, 4, 4, 7, 9, 7, 5, 2, 1, 6, 2, 6, 7, 2, 8, 7, 1, 6, 2, 1, 2, 2, 3, 4, 2, 7, 3, 8, 3, 8, 4, 6, 5, 5, 7, 1, 6, 5, 7, 4, 5, 4, 6, 2, 2, 3, 8, 2, 9, 3, 2, 5, 3, 8, 4, 1, 2, 2, 5, 4, 1, 5, 1, 5, 4, 4, 6, 3, 3, 5, 5, 3, 4, 2, 3, 2, 6, 3, 3, 3, 6, 8, 4, 6, 6, 4, 1, 4, 2, 5, 7, 3, 4, 2, 4, 4, 3, 4, 5, 8, 6, 1, 3, 1, 1, 1, 4, 3, 4, 5, 2, 4, 2, 3, 4, 5, 2, 2, 3, 3, 4, 3, 7, 7, 6, 3, 3, 7, 4, 2, 2, 2, 4, 2, 3, 3, 5, 4, 2, 3, 1, 2, 2, 1, 6, 3, 1, 6, 3, 2, 1, 2, 3, 4, 1, 7, 6, 1, 3, 2, 5, 1, 3, 2, 1, 2, 3, 3, 5, 4, 2, 2, 3, 4, 1, 3, 2, 2, 1, 1, 3, 5, 4, 1, 3, 3, 2, 5, 2, 3, 2, 2, 2, 1, 1, 1, 2, 4, 2, 4, 4, 3, 4, 3, 2, 3, 3, 4, 1, 4, 1, 3, 2, 2, 3, 2, 3, 5, 1, 2, 1, 2, 5, 1, 3, 3, 3, 6, 3, 4, 2, 4, 5, 3, 3, 1, 1, 2, 3, 1, 2, 2, 2, 5, 2, 2, 5, 2, 2, 2, 6, 2, 2, 3, 1, 2, 2, 1, 3, 2, 4, 4, 3, 2, 2, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 3, 1, 2, 3, 1, 5, 4, 6, 2, 4, 1, 1, 4, 1, 2, 3, 2, 4, 2, 3, 2, 1, 7, 3, 3, 3, 2, 2, 2, 3, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 4, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 2, 1, 3, 2, 1, 2, 1, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 3, 3, 1, 3, 1, 1, 1, 1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 3, 2, 1, 2, 2, 1, 1, 1, 2, 1, 1, 1, 2, 1, 1, 2, 3, 1, 2, 3, 3, 1, 1, 1, 1, 1, 2, 2, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 1, 2, 3, 1, 2, 1, 1, 3, 1, 1, 2, 2, 1, 1, 4, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 1, 4, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 1, 1, 2, 3, 1, 1, 2, 1, 1, 1, 2, 2, 1, 2, 1, 1, 1, 1, 2, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 2, 1, 1, 3, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 3, 2, 1, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1]

    #ages
    # x =  [0.0, 0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.19, 0.2, 0.21, 0.22, 0.23, 0.24, 0.25, 0.26, 0.27, 0.28, 0.31, 0.32, 0.34, 0.39, 14.92, 15.06, 15.18, 15.19, 15.21, 15.22, 15.25, 15.7, 15.85, 16.02, 16.03, 16.07, 16.21, 16.29, 16.36, 16.39, 16.44, 16.48, 16.51, 16.63, 16.79, 16.82, 16.84, 16.91, 16.93, 16.95, 16.98, 16.99, 17.02, 17.03, 17.04, 17.07, 17.08, 17.13, 17.16, 17.18, 17.2, 17.21, 17.23, 17.24, 17.25, 17.29, 17.31, 17.33, 17.34, 17.35, 17.37, 17.38, 17.39, 17.41, 17.44, 17.57, 17.61, 17.62, 17.64, 17.65, 17.68, 17.72, 17.74, 17.78, 17.79, 17.82, 17.83, 17.84, 17.85, 17.86, 17.88, 17.9, 17.92, 17.95, 17.96, 17.98, 17.99]
    # y =  [7366, 602, 40, 12, 9, 4, 7, 7, 3, 4, 5, 1, 5, 2, 2, 5, 1, 2, 1, 1, 2, 2, 3, 1, 1, 1, 1, 2, 1, 4, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 1, 1, 1, 2, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 2, 1, 1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 1, 1, 1, 1, 2, 4, 1, 1, 1, 1, 2, 3, 1, 2, 2, 1, 1]

    #component spelling ratios
    x = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    y = [0.81999999999999995, 0.85999999999999999, 0.80000000000000004, 0.77000000000000002, 0.31578947368421051, 0.4925581395348837, 0.25806451612903225, 0.39230769230769236, 0.21739130434782608, 0.17424242424242425]
    return x, y

def scatter(x, y, title, xlabel, ylabel, xlabel_rotation=45):
    fig, ax = plt.subplots()
    ax.set_yscale('log')
    # ax.set_xscale('log')
    # ax.set_xscale('log')
    # add some text for labels, title and axes ticks
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # plt.xticks(np.arange(19), tuple(xrange(0,19)))
    # ax.set_xticklabels(tuple(xrange(0,19)), rotation=xlabel_rotation)

    plt.scatter(x, y)
    plt.show()

def line(x, y, title, xlabel, ylabel, xlabel_rotation=45):
    fig, ax = plt.subplots()
    # ax.set_yscale('log')
    # ax.set_xscale('log')
    # ax.set_xscale('log')
    # add some text for labels, title and axes ticks
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    # plt.xticks(np.arange(19), tuple(xrange(0,19)))
    # ax.set_xticklabels(tuple(xrange(0,19)), rotation=xlabel_rotation)

    plt.plot(x, y, linestyle="solid")
    plt.show()

"""
data: list of (x, y) tuples
"""
def histogram(data, title, xlabel, ylabel, xlabel_rotation=90):
    months = []
    num_posts_per_month = []

    for m, p in data:
        months.append(m)
        num_posts_per_month.append(p)

    N = len(months)

    ind = np.arange(N)  # the x locations for the groups
    width = 0.35       # the width of the bars

    fig, ax = plt.subplots()

    rects = ax.bar(ind, tuple(num_posts_per_month), width)

    # add some text for labels, title and axes ticks
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)

    ax.set_xticks(ind + width / 2)
    # ax.set_yscale('log')

    tl = plt.gca().get_xticklabels()
    maxsize = max([t.get_window_extent().width for t in tl])
    m = 0.2 # inch margin
    s = maxsize/plt.gcf().dpi*N+2*m
    margin = m/plt.gcf().get_size_inches()[0] * 2

    plt.gcf().subplots_adjust(left=margin, right=1.-margin)
    plt.gcf().set_size_inches(s, plt.gcf().get_size_inches()[1])

    ax.set_xticklabels(tuple(months), rotation=xlabel_rotation)
    # plt.savefig('posts-per-month.png', bbox_inches='tight')
    plt.show()

if __name__ == '__main__':
    x, y = load_data()
    line(x, y, 'Ratio of Correctly Spelled Words', 'Number of Components', '# Correctly Spelled / Total Words', xlabel_rotation=45)

    # scatter(x, y, 'Number of Words per Note', 'Number of Words', 'Number of Notes', xlabel_rotation=45)

    # scatter(x, y, 'Number of Notes per Patient', 'Number of Notes', 'Number of Patients', xlabel_rotation=45)

    # scatter(x, y, 'Number of Stays by Age', 'Ages', 'Number of Stays', xlabel_rotation=45)

    # scatter(x, y, 'ICU Children Age Breakdown', 'Ages', 'Number of Children', xlabel_rotation=45)
    # histogram([(0, 7870), (14, 1), (15, 8), (16, 22), (17, 67)], \
    #             'ICU Children Age Breakdown', 'Ages', 'Number of Children', xlabel_rotation=45)
