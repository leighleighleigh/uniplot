import numpy as np  # type: ignore
from typing import List, Optional

from uniplot.discretizer import discretize

LEFT_MARGIN_FOR_HORIZONTAL_AXIS = 1


class LabelSet:
    """
    This class represents a list of possible axis labels. It can render them to a string, or list of strings. It also provides metrics about the rendering result.
    """

    def __init__(
        self,
        labels: np.array,
        x_min: float,
        x_max: float,
        available_space: int,
        vertical_direction: bool = False,
    ):
        self.labels = labels
        self.x_min = x_min
        self.x_max = x_max
        self.available_space = available_space
        self.vertical_direction = vertical_direction
        self._results_already_in_cache: bool = False
        self._rendered_result: List[str] = []
        self._render_does_overlap: bool = False

    def render(self) -> List[str]:
        self._render_and_measure_to_cache()
        return self._rendered_result

    def compute_if_render_does_overlap(self) -> bool:
        self._render_and_measure_to_cache()
        return self._render_does_overlap

    ###########
    # private #
    ###########

    def _render_and_measure_to_cache(self) -> None:
        # Break if result is already in cache
        if self._results_already_in_cache:
            return

        str_labels = self._find_shortest_string_representation(self.labels)
        line = ""
        for i, label in enumerate(self.labels):
            str_label = str_labels[i]
            offset = max(
                0,
                discretize(
                    label,
                    x_min=self.x_min,
                    x_max=self.x_max,
                    steps=self.available_space,
                )
                - int(0.5 * len(str_label))
                + LEFT_MARGIN_FOR_HORIZONTAL_AXIS,
            )
            buffer = offset - len(line)
            if i == 0 and buffer < 0:
                # This is bad and leads to wrong offsets
                buffer = 0
                self._render_does_overlap = True
            elif i > 0 and buffer < 1:
                # This is bad and leads to wrong offsets
                buffer = 1
                self._render_does_overlap = True

            line = line + (" " * buffer) + str_label

        self._rendered_result = [line]
        self._results_already_in_cache = True

    def _find_shortest_string_representation(
        self,
        numbers: List[Optional[float]],
    ) -> List[str]:
        """
        This method will find the shortest numerical values for axis labels that are different from ech other.
        """
        # We actually want to add one more digit than needed for uniqueness
        for nr_digits in range(10):
            test_list = [
                self._float_format(n, nr_digits) for n in numbers if n is not None
            ]
            if len(test_list) == len(set(test_list)):
                return [
                    "" if n is None else self._float_format(n, nr_digits)
                    for n in numbers
                ]

        # Fallback to naive string conversion
        return ["" if n is None else str(n) for n in numbers]

    def _float_format(self, n: float, nr_digits: int):
        """
        Format a number to a specified precision.

        Ref.: https://docs.python.org/3.8/library/string.html#format-specification-mini-language
        """
        if nr_digits == 0:
            return ("{:,d}").format(int(n))
        return ("{:,." + str(nr_digits) + "g}").format(float(n))
