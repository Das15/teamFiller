import objects.bracket as bracket
import objects.ladder_legacy as ladder_legacy
import objects.mappool as mappool
import objects.match as match


def extract_round_names(rounds) -> list[str]:
    names = []
    for entry in rounds:
        if entry.Name not in names:
            if entry.Name == "":
                names.append(entry.Description)
                continue
            names.append(entry.Name)
    return names


def scan_matches(bracket_data, round_names) -> list[list[mappool.Class]]:
    ladder_tree = []
    for i in range(len(round_names)):
        ladder_tree.append([])
    for i in range(len(round_names)):
        for entry in bracket_data.Matches:
            if entry.ID in bracket_data.Rounds[i].Matches:
                ladder_tree[i].append(entry)
        ladder_tree[i].sort(key=lambda x: x.ID)
        if i >= 2 and len(ladder_tree[i]) >= 3:
            amounf_of_moved_matches = 0
            j = int(len(ladder_tree[0]) / pow(2, i)) - 1
            while j < len(ladder_tree[i]) - amounf_of_moved_matches - 1:
                j += 2
                ladder_tree[i].insert(len(ladder_tree[i]), ladder_tree[i].pop(j))
                amounf_of_moved_matches += 1
    return ladder_tree


class Class(object):
    def __init__(self, bracket_data: bracket.Class):
        self.roundNames = extract_round_names(bracket_data.Rounds)
        self.ladder = scan_matches(bracket_data, self.roundNames)

    # TODO: Remove or use this function
    def get_matches(self):
        matches = []
        for mappoolRound in self.ladder:
            for entry in mappoolRound:
                matches.append(entry)
        return matches

    # TODO: Make function just a bit more readable
    def get_match_from_identifier(self, challonge_match_id: int) -> match.Class | None:
        amount_of_winner_matches = len(self.ladder[0]) * 2
        amount_of_passed_winner_matches = 0
        total_amount_of_passed_matches = 0
        max_round_match_id = amount_of_winner_matches / 2

        for matches in self.ladder:
            total_amount_of_passed_matches += len(matches)

            if challonge_match_id <= amount_of_winner_matches:  # Winner's bracket
                if challonge_match_id <= max_round_match_id + amount_of_passed_winner_matches:
                    match_id = challonge_match_id - amount_of_passed_winner_matches
                    return matches[match_id - 1]

            else:  # Loser's bracket
                if matches is self.ladder[1]:
                    if challonge_match_id <= total_amount_of_passed_matches + len(matches) / 2 + 1:
                        match_id = challonge_match_id - amount_of_winner_matches + int(len(matches) / 2) - 2
                        return matches[match_id]

                if matches is not self.ladder[0] and matches is not self.ladder[1]:
                    if challonge_match_id <= total_amount_of_passed_matches + len(matches) / 4 + 1:
                        match_id = challonge_match_id - total_amount_of_passed_matches + len(matches) - \
                                  int(max_round_match_id * 2) - 2 + int(max_round_match_id)
                        if matches is self.ladder[-1]:
                            return matches[-2]
                        return matches[match_id]
            amount_of_passed_winner_matches += int(max_round_match_id)
            max_round_match_id /= 2

        if challonge_match_id == amount_of_winner_matches:
            return self.ladder[-1][0]
        return None

    def get_match(self, challonge_match_id: int, is_identifier: bool = False) -> match.Class | None:
        if is_identifier:
            return self.get_match_from_identifier(challonge_match_id)
        return ladder_legacy.get_match_from_suggested_order(self, challonge_match_id)
