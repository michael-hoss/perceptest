import sys
from dataclasses import dataclass


@dataclass
class AABoundingBox:
    # Axis-aligned bounding box
    # By default, initialize with largest negative volume to grow it from there
    x_min: float = sys.float_info.max
    x_max: float = -sys.float_info.max
    y_min: float = sys.float_info.max
    y_max: float = -sys.float_info.max

    def include_point(self, x: float, y: float) -> "AABoundingBox":
        self.x_min = min(self.x_min, x)
        self.x_max = max(self.x_max, x)
        self.y_min = min(self.y_min, y)
        self.y_max = max(self.y_max, y)
        return self

    def is_contained_in(self, outer: "AABoundingBox") -> bool:
        return (
            outer.x_min <= self.x_min
            and outer.x_max >= self.x_max
            and outer.y_min <= self.y_min
            and outer.y_max >= self.y_max
        )

    def include_aa_bounding_box(self, other: "AABoundingBox") -> "AABoundingBox":
        self.x_min = min(self.x_min, other.x_min)
        self.x_max = max(self.x_max, other.x_max)
        self.y_min = min(self.y_min, other.y_min)
        self.y_max = max(self.y_max, other.y_max)
        return self

    def is_larger_than_min_span(self, x: float, y: float) -> bool:
        return (self.x_max - self.x_min) >= x and (self.y_max - self.y_min) >= y

    def is_smaller_than_max_span(self, x: float, y: float) -> bool:
        return (self.x_max - self.x_min) <= x and (self.y_max - self.y_min) <= y

    @property
    def center_x(self) -> float:
        return (self.x_min + self.x_max) / 2

    @property
    def center_y(self) -> float:
        return (self.y_min + self.y_max) / 2

    @property
    def span_x(self) -> float:
        return self.x_max - self.x_min

    @property
    def span_y(self) -> float:
        return self.y_max - self.y_min

    def center_is_within(self, center_bounds: "AABoundingBox") -> bool:
        return (
            center_bounds.x_min <= self.center_x
            and center_bounds.x_max >= self.center_x
            and center_bounds.y_min <= self.center_y
            and center_bounds.y_max >= self.center_y
        )
