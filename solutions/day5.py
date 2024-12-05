from utils import read_file_as_lines


def get_rules_and_updates(input_path):
    data = read_file_as_lines(input_path)
    rules = []
    updates = []
    reading_rules = True
    for line in data:
        if line == "":
            reading_rules = False
            continue
        if reading_rules:
            assert "|" in line
            rules.append(tuple([int(num) for num in line.split("|")]))
        else:
            updates.append(tuple([int(num) for num in line.split(",")]))

    rules_lookup = {}
    for before, after in rules:
        rules_lookup.setdefault(before, {"before": set(), "after": set()})
        rules_lookup.setdefault(after, {"before": set(), "after": set()})
        rules_lookup[before]["after"].add(after)
        rules_lookup[after]["before"].add(before)
    
    return rules_lookup, updates


def part1(input_path):

    rules_lookup, updates = get_rules_and_updates(input_path)

    correct_updates = []
    centre_numbers = []

    for update in updates:
        failed = False
        for i, num in enumerate(update):
            nums_before = set(update[0:i])
            nums_after = set(update[i + 1:])
            lookup = rules_lookup[num]
            if (nums_after - lookup["after"]) or (nums_before - lookup["before"]):
                failed = True
                break
        if not failed:
            correct_updates.append(update)
            assert len(update) % 2 == 1
            centre_num = update[len(update) // 2]
            centre_numbers.append(centre_num)
    
    print(sum(centre_numbers))


def part2(input_path):

    rules_lookup, updates = get_rules_and_updates(input_path)

    incorrect_updates = []
   
    def is_valid(num, i, update):
        nums_before = set(update[0:i])
        nums_after = set(update[i + 1:])
        lookup = rules_lookup[num]
        return not ((nums_after - lookup["after"]) or (nums_before - lookup["before"]))
    
    for update in updates:
        for i, num in enumerate(update):
            if not is_valid(num, i, update):
                incorrect_updates.append(update)
                break
    
    centre_nums = []
    for update in incorrect_updates:
        # start with first item
        sorted_update = [update[0]]
        # all rules
        update_rules = {k: v for k, v in rules_lookup.items() if k in update}
        # loop through update list from second item
        for num in update[1:]:
            before = update_rules[num]["before"]
            after = update_rules[num]["after"]
            found_before = set(sorted_update) & before
            found_after = set(sorted_update) & after

            if found_before:
                # found some elements in the sorted_update list that must be before this one
                max_index = max([sorted_update.index(x) for x in found_before])
                sorted_update.insert(max_index + 1, num)
            elif found_after:
                # found some elements in the sorted_update list that must come sfter this one
                min_index = min([sorted_update.index(x) for x in found_after])
                if min_index == 0:
                    sorted_update = [num] + sorted_update
                else:
                    sorted_update.insert(min_index - 1, num)
            if not (found_before or found_after):
                assert False
        
        assert len(sorted_update) == len(update), (update, sorted_update)
        assert len(sorted_update) % 2 == 1
        centre_num = sorted_update[len(sorted_update) // 2]
        centre_nums.append(centre_num)
    
    print(sum(centre_nums))
