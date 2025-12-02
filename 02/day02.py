# load data
class Range:
    start: int
    stop: int

    def find_invalid_ids_partB(self):
        # invalid is every id that is made of only repeating sequences (at least twice)
        size_start = len(str(self.start))
        size_end = len(str(self.stop))

        # get all divisors of size_start and size_end
        invalid_ids = set()
        for n in range(size_start, size_end + 1):
            divisors = set()
            for i in range(1, n + 1):
                if n % i == 0:
                    divisors.add(i)
            # for each divisor, generate repeating sequences and check if they are in the range

            for div in divisors:
                if div == n:
                    continue
                repeat_count = n // div
                for seq in range(10 ** (div - 1), 10**div + 1):
                    seq_str = str(seq)
                    num_str = seq_str * repeat_count
                    num = int(num_str)
                    #  print(f"Seq: {seq}, Generated number: {num}")
                    if num >= self.start and num <= self.stop:
                        invalid_ids.add(num)

        return sorted(list(invalid_ids))

    def find_invalid_ids_partA(self):
        size_start = len(str(self.start))
        size_end = len(str(self.stop))

        result = self.drop_part_of_range_with_uneven_digits(size_start, size_end)

        if result is None:
            return []
        else:
            self.start, self.stop = result

        size_start = len(str(self.start))
        size_end = len(str(self.stop))
        # print(f"Adjusted Range: {self.start}-{self.stop}")
        invalid_ids = []
        # efficient checking means splitting in two parts, only checking the few numbers on the left against the range on the right
        left_min = str(self.start)[: size_start // 2]
        left_max = str(self.stop)[: size_end // 2]

        right_min = int(str(self.start)[size_start // 2 :])
        right_max_temp = str(self.stop)[size_end // 2 :]

        diff = int(left_max) - int(left_min)

        right_max = int(right_max_temp) + diff * (10 ** (size_end // 2))

        # print(left_min, left_max, right_min, right_max)

        for delta in range(0, int(left_max) - int(left_min) + 1):
            # check against right from right min to diff * 10^(size_end/2) + right max, not by iterating all numbers but by bounds check
            left = int(left_min) + delta
            right = int(str(delta) + str(left))
            if right >= right_min and right <= right_max:
                invalid_ids.append(int(str(left) + str(left)))
        return invalid_ids

    def drop_part_of_range_with_uneven_digits(self, size_start, size_stop):
        if size_start == size_stop:
            if size_start % 2 == 0:
                return (self.start, self.stop)
            else:
                return None
        # start has even digits, so keep start till max number with same digits
        if size_start % 2 == 0:
            max_num = int("9" * size_start)
            new_start = self.start
            new_stop = max_num
            return (new_start, new_stop)
        # stop has even digits, so keep min number with same digits till stop
        if size_stop % 2 == 0:
            min_num = int("1" + "0" * (size_stop - 1))
            new_start = min_num
            new_stop = self.stop
            return (new_start, new_stop)


with open("02/input.txt") as f:
    data = f.read().splitlines()[0]

invalids_A = []
invalids_B = []
for startstop in data.split(","):
    start, stop = map(int, startstop.split("-"))
    r = Range()
    r.start = start
    r.stop = stop

    inv_B = r.find_invalid_ids_partB()
    invalids_B.extend(inv_B)
    print(f"Range: {start}-{stop}, Invalid IDs Part B: {inv_B}")

    inv_A = r.find_invalid_ids_partA()
    invalids_A.extend(inv_A)
    print(f"Range: {start}-{stop}, Invalid IDs: {inv_A}")

print(f"part A) Sum of all invalid IDs: {sum(invalids_A)}")
print(f"part B) Sum of all invalid IDs: {sum(invalids_B)}")
