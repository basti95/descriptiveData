from typing import Tuple, Any, List, Dict, Union

import pandas
from numpy import ndarray
from pandas import Series, Index
from scipy.signal import find_peaks


class Metric:
    def __init__(self, series: pandas.Series, fillna: float = 0) -> None:  # noqa
        # Remove NaNs to avoid unpredictable behaviour
        if series.hasnans:
            series = series.fillna(fillna or 0)
        self.data = series

    def get_max(self) -> Dict[str, Union[Index, Any]]:
        return {'x': self.data.idxmax(), 'y': self.data.max()}

    def get_local_max(self) -> List[Dict[str, Any]]:
        peaks, _ = find_peaks(self.data.values, height=0)
        return [{'x': peak, 'y': self.data[peak]} for peak in peaks.tolist()]
