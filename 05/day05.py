from collections import deque


class Range:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def contains(self, other: "Range") -> bool:
        return self.start <= other.start and self.end >= other.end

    def overlaps(self, other: "Range") -> tuple[bool, int]:
        overlap_size = min(self.end, other.end) - max(self.start, other.start) + 1
        return self.start <= other.end and other.start <= self.end, overlap_size

    def number_is_in_range(self, number: int) -> bool:
        return self.start <= number <= self.end

    def get_size(self) -> int:
        return self.end - self.start + 1

    @classmethod
    def from_string(cls, range_str: str) -> "Range":
        start_str, end_str = range_str.split("-")
        return cls(int(start_str), int(end_str))


with open("05/input.txt") as f:
    data = f.read().strip()
    fresh_ranges, ingredients = data.split("\n\n")

fresh_ranges = [Range.from_string(line.strip()) for line in fresh_ranges.split("\n")]
ingredients = [int(line.strip()) for line in ingredients.split("\n")]


fresh_ingredients = 0
for ingredient in ingredients:
    if any(r.number_is_in_range(ingredient) for r in fresh_ranges):
        fresh_ingredients += 1
print("A) ", fresh_ingredients)

#### PART B ####
# merge overlapping ranges
# sort fresh ranges by start
# make a deque for easy popping from left
sorted_fresh_ranges = deque(sorted(fresh_ranges, key=lambda r: r.start))
merged_ranges = []
while sorted_fresh_ranges:
    # get current range from left and copare against all others
    current_range = sorted_fresh_ranges.popleft()
    for other in list(sorted_fresh_ranges):
        # if the ranges overlap, merge them and remove the other from the deque
        if current_range.overlaps(other)[0]:
            # merge ranges
            current_range = Range(
                start=min(current_range.start, other.start),
                end=max(current_range.end, other.end),
            )
            sorted_fresh_ranges.remove(other)
    # add the (possibly merged) current range to the merged ranges list
    merged_ranges.append(current_range)

adjusted_total_size = sum(r.get_size() for r in merged_ranges)
print("B) ", adjusted_total_size)
