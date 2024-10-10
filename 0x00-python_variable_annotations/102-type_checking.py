#!/usr/bin/env python3
'''
safas sfasf fgsdg dgsg sdgsdg
'''
from typing import List, Tuple


def zoom_array(lst: Tuple, factor: int = 2) -> List:
    '''
    dgsdgsdg dsgs dgsdg sdg dsgsdgsdg
    '''
    zoomed_in: List = [
        item for item in lst
        for i in range(factor)
    ]
    return zoomed_in


array = (12, 72, 91)

zoom_2x = zoom_array(array)

zoom_3x = zoom_array(array, 3)
