import objects.match as match

# TODO: Refactor this file, it's a mess, I know


def get_match_from_fourth_round(ladder_obj, match_index, middle_index, pool_length) -> match.Class:
    if match_index >= middle_index / 2:
        return ladder_obj.ladder[3][match_index]
    if match_index >= 0:
        return ladder_obj.ladder[3][match_index + middle_index]
    if match_index >= -pool_length / 2:
        return ladder_obj.ladder[3][match_index - int(pool_length / 2)]
    return ladder_obj.ladder[3][match_index + int(pool_length / 2)]


def get_match_from_fifth_round(ladder_obj, match_index, middle_index, pool_length) -> match.Class:
    if match_index < -pool_length:
        return ladder_obj.ladder[4][match_index]
    if -pool_length <= match_index < 0:
        return ladder_obj.ladder[4][match_index + middle_index]
    match_index = -match_index - int(pool_length / 2)
    if pool_length == 1:
        match_index = -match_index
    return ladder_obj.ladder[4][match_index]


# Leaving this just in case something changes on challonge API side and I'll have to scan matches using suggested order
# Also i have no clue on what i wrote here, since it works i assume it's fine.
# TODO: refactor it or something, idk
def get_match_from_suggested_order(ladder_obj, challonge_match_id: int) -> match.Class | None:
    internal_match_id = challonge_match_id - 1
    pool_length = len(ladder_obj.ladder[0])
    i = 0
    passed_matches_count = 0
    checks_fulfilled = 0
    # Why the fuck is this loop so hard to read?
    while checks_fulfilled < 3:
        if i == 0:
            if challonge_match_id <= pool_length:
                return ladder_obj.ladder[i][internal_match_id]
            passed_matches_count = pool_length
        else:
            if checks_fulfilled == 0:
                passed_matches_count += pool_length * 2 if i == 1 else pool_length * 4
            else:
                passed_matches_count += 1
            if challonge_match_id <= passed_matches_count:
                # Offset what? Why did i make it like this? I don't get it
                offset = passed_matches_count - pool_length
                match_count = pool_length * 4
                if checks_fulfilled > 1:
                    match_count -= 1
                middle_index = int(match_count / 2)
                if i % 2 == 0:
                    if challonge_match_id > offset and i != len(ladder_obj.ladder) - 1:
                        return ladder_obj.ladder[i][internal_match_id - passed_matches_count + pool_length]
                    if i == 4:
                        match_index = internal_match_id - passed_matches_count + middle_index
                        return get_match_from_fifth_round(ladder_obj, match_index, middle_index, pool_length)
                    match_index = -challonge_match_id + passed_matches_count - pool_length
                    if match_index < pool_length:
                        match_index = -challonge_match_id + passed_matches_count - middle_index
                    return ladder_obj.ladder[i][match_index]

                if challonge_match_id > offset:
                    return ladder_obj.ladder[i][internal_match_id - passed_matches_count + pool_length]
                if i == 3:
                    match_index = -challonge_match_id + passed_matches_count - middle_index
                    return get_match_from_fourth_round(ladder_obj, match_index, middle_index, pool_length)
                return ladder_obj.ladder[i][internal_match_id - passed_matches_count + pool_length]
        i += 1
        pool_length = int(pool_length / 2)
        if pool_length < 1:
            checks_fulfilled += 1
            pool_length = 1
        i = i if i < len(ladder_obj.ladder) else len(ladder_obj.ladder) - 1
    if challonge_match_id == len(ladder_obj.ladder[0]) * 4 - 1:
        return ladder_obj.ladder[i][-1]
    return None
