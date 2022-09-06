import copy
import unittest
import ps1

def check_valid_mapping(election, move_voters_result, real_results):
    # case when student returns None
    if move_voters_result is None:
        assert real_results is None, "You return None, but there is a possible solution here."
        return True

    if real_results is None:
        assert move_voters_result is None, "This election cannot be flipped, we expected you to return None"
        return True

    voter_map, ec_votes, voters_moved = move_voters_result
    staff_voter_map, staff_ec_votes, staff_voters_moved = real_results
    orig_winner_states = ps1.get_winner_states(election)
    orig_winner, orig_loser = ps1.find_winner(election)
    election_copy = election[:]
    
    # check if the numbers line up
    assert (ec_votes == staff_ec_votes), "The number of ec_votes gained isn't quite right: you got %s, we expected %s" %(ec_votes, staff_ec_votes)
    assert (voters_moved == staff_voters_moved), "The number of voters_moved isn't quite right you got %s, we expected %s" %(voters_moved, staff_voters_moved)

    # maps the state to the index in the list allows for easy access
    election_dict = {}
    for state_index in range(len(election_copy)):
        election_dict[election_copy[state_index].get_name()] = state_index 

    # make all of the move's suggested in voter_map 
    for state_from, state_to in voter_map:
        from_index, to_index = election_dict[state_from], election_dict[state_to]
        from_margin, to_margin = election_copy[from_index].get_margin(), election_copy[to_index].get_margin()
        margin_moved = voter_map[(state_from, state_to)]

        # just flipped a state that was already won
        assert from_margin-margin_moved >= 1, "You lost/tied a State, %s, that was originally won by the winner." %state_from
        
        assert state_from not in ['WA', 'CA', 'TX', 'TN'], "You moved residents from a state,%s, you weren't allowed to move from." %state_from
            
        #change the results of the election
        election_copy[from_index].margin = from_margin-margin_moved
        if to_margin - margin_moved < 0:
            election_copy[to_index].margin = abs(to_margin-margin_moved)
            election_copy[to_index].winner = orig_loser
        else:
            election_copy[to_index].margin = to_margin-margin_moved

    # check if after all of the changes are made, the election result has been flipped 
    new_winner, new_loser = ps1.find_winner(election_copy)
    assert new_winner == orig_loser, "After making the moves you suggested, the election has not been flipped"
    return True 

class TestPS1(unittest.TestCase):
    def test_1_state_class(self):
        state_1 = ps1.State("MA", 100000, 20000, 8)
        state_2 = ps1.State("NY", 123456, 7890, 25)
        state_1_dup = ps1.State("MA", 100000, 20000, 8)

        self.assertIsInstance(state_1, ps1.State, "The class did not return an instance of State, but instead an instance of %s." % type(state_1))
        self.assertTrue(hasattr(state_1, 'name'), "The name attribute was not instantiated in the State object.")
        self.assertTrue(hasattr(state_1, 'margin'), "The margin attribute was not instantiated in the State object.")
        self.assertTrue(hasattr(state_1, 'winner'), "The winner attribute was not instantiated in the State object.")
        self.assertTrue(hasattr(state_1, 'ec'), "The ec attribute was not instantiated in the State object.")
        self.assertEqual(state_1.get_name(), "MA", "The get_name() function was not implemented correctly.")
        self.assertEqual(state_1.get_num_ecvotes(), 8, "The get_num_ecvotes() function was not implemented correctly.")
        self.assertEqual(state_1.get_margin(), abs(100000-20000), "The get_margin() function was not implemented correctly.")
        self.assertEqual(state_1.get_winner(), "dem", "The get_winner() function was not implemented correctly.")
        self.assertEqual(state_1, state_1_dup, "The __eq__ function was not implemented correctly.")
        self.assertIsInstance(state_1_dup, ps1.State, "The __eq__ function was not implemented correctly.")
        self.assertNotEqual(state_1, state_2, "The __eq__ function was not implemented correctly.")

    def test_2_load_election(self):
        election_600 = ps1.load_election("600_results.txt")
        real_election = [ps1.State("TX",1,2,530), ps1.State("CA",4,5,3), ps1.State("MA",7,8,5)]

        self.assertIsInstance(election_600, list, "load_electiondid not return a list, but instead returned an instance of %s." % type(election_600))
        self.assertEqual(len(election_600), 3, "The length of the list returned by load_electionis not correct. Expected %s, got %s." % (3, len(election_600)))
        self.assertTrue(all(isinstance(st, ps1.State) for st in election_600), "An item in the list returned by load_election is not a State instance. The item you returned is: %s" % election_600)
        self.assertTrue(all(election_600[i] == real_election[i] for i in range(len(election_600))), "The list returned by load_election does not match the expected list. \nExpected: %s \nGot: %s " % (real_election, election_600))

    def test_3_find_winner(self):
        gop_won = ("gop", "dem")
        dem_won = ("dem", "gop")
        results_2016 = ps1.find_winner(ps1.load_election("2016_results.txt"))
        results_2012 = ps1.find_winner(ps1.load_election("2012_results.txt"))
        results_2008 = ps1.find_winner(ps1.load_election("2008_results.txt"))
        real_election = [ps1.State("TX",2,1,100), ps1.State("CA",1,2,1), ps1.State("MA",1,2,2)]
        results_real = ps1.find_winner(real_election)
        self.assertEqual(results_2016, gop_won, "The tuple returned by find_winner does not have the correct number of items. Expected %s, got %s." % (2, len(results_2016)))
        self.assertEqual(results_real, dem_won, "For a sample election: expected %s, got %s. You appear to be tallying number of states won rather than number of EC votes won by a state." % (gop_won, results_real))
        self.assertEqual(results_2016, gop_won, "For the 2016 election: expected %s, got %s." % (gop_won, results_2016))
        self.assertEqual(results_2012, dem_won, "For the 2012 election: expected %s, got %s." % (gop_won, results_2012))
        self.assertEqual(results_2008, dem_won, "For the 2008 election: expected %s, got %s." % (gop_won, results_2008))
        
    def test_3_get_winner_states(self):
        real_600 = set(['TX', 'CA', 'MA'])
        real_2016 = set(['AL', 'AK', 'AZ', 'AR', 'FL', 'GA', 'ID', 'IN', 'IA', 'KS', 'KY', 'LA', 'MI', 'MS', 'MO', 'MT', 'NE', 'NC', 'ND', 'OH', 'OK', 'PA', 'SC', 'SD', 'TN', 'TX', 'UT', 'WV', 'WI', 'WY'])
        real_2012 = set(['CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'HI', 'IL', 'IA', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'OH', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])
        real_2008 = set(['CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'HI', 'IL', 'IN', 'IA', 'ME', 'MD', 'MA', 'MI', 'MN', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'OH', 'OR', 'PA', 'RI', 'VT', 'VA', 'WA', 'WI'])

        results_600 = [state.get_name() for state in ps1.get_winner_states(ps1.load_election("600_results.txt"))]
        results_2016 = [state.get_name() for state in ps1.get_winner_states(ps1.load_election("2016_results.txt"))]
        results_2012 = [state.get_name() for state in ps1.get_winner_states(ps1.load_election("2012_results.txt"))]
        results_2008 = [state.get_name() for state in ps1.get_winner_states(ps1.load_election("2008_results.txt"))]

        self.assertTrue(type(results_600) == list, "Please return a list")
        self.assertEqual(len(results_600), len(set(results_600)), "Duplicate states found in list")
        self.assertEqual(len(results_2016), len(set(results_2016)), "Duplicate states found in list")
        self.assertEqual(len(results_2012), len(set(results_2012)), "Duplicate states found in list")
        self.assertEqual(len(results_2008), len(set(results_2008)), "Duplicate states found in list")

        self.assertEqual(real_600, set(results_600),  "For the sample election: expected %s, got %s." % (real_600, results_600))
        self.assertEqual(real_2016, set(results_2016), "For the 2016 election: expected %s, got %s." % (real_2016, results_2016))
        self.assertEqual(real_2012, set(results_2012), "For the 2012 election: expected %s, got %s." % (real_2012, results_2012))
        self.assertEqual(real_2008, set(results_2008), "For the 2008 election: expected %s, got %s." % (real_2008, results_2008))


    def test_3_ec_votes_reqd(self):
        real_600 = 270
        real_2016 = 37
        real_2012 = 64
        real_2008 = 96
        results_600 = ps1.ec_votes_reqd(ps1.load_election("600_results.txt"))
        results_2016 = ps1.ec_votes_reqd(ps1.load_election("2016_results.txt"))
        results_2012 = ps1.ec_votes_reqd(ps1.load_election("2012_results.txt"))
        results_2008 = ps1.ec_votes_reqd(ps1.load_election("2008_results.txt"))

        self.assertEqual(results_600, real_600, "For the sample election: expected %s, got %s." %(real_600, results_600) )
        self.assertEqual(results_2016, real_2016, "For the 2016 election: expected %s, got %s." % (real_2016, results_2016))
        self.assertEqual(results_2012, real_2012, "For the 2012 election: expected %s, got %s." % (real_2012, results_2012))
        self.assertEqual(results_2008, real_2008, "For the 2008 election: expected %s, got %s." % (real_2008, results_2008))
   
    def test_4_greedy_election(self):
        real_sample = set(['TX'])
        real_2016 = set(['MI', 'WI', 'PA'])
        real_2012 = set(['NH', 'NV', 'FL', 'DE', 'NM', 'IA', 'VT', 'ME', 'RI'])
        real_2008 = set(['NC', 'IN', 'NH', 'DE', 'VT', 'NV', 'NM', 'ME', 'RI', 'IA', 'HI', 'CO', 'DC', 'VA', 'FL'])
        lost_sample = ps1.get_winner_states(ps1.load_election("600_results.txt"))
        lost_2016 = ps1.get_winner_states(ps1.load_election("2016_results.txt"))
        lost_2012 = ps1.get_winner_states(ps1.load_election("2012_results.txt"))
        lost_2008 = ps1.get_winner_states(ps1.load_election("2008_results.txt"))
        votes_sample = ps1.ec_votes_reqd(ps1.load_election("600_results.txt"))
        votes_2016 = ps1.ec_votes_reqd(ps1.load_election("2016_results.txt"))
        votes_2012 = ps1.ec_votes_reqd(ps1.load_election("2012_results.txt"))
        votes_2008 = ps1.ec_votes_reqd(ps1.load_election("2008_results.txt"))
        results_sample_list = ps1.greedy_election(lost_sample,votes_sample)
        results_2016_list = ps1.greedy_election(lost_2016,votes_2016)
        results_2012_list = ps1.greedy_election(lost_2012,votes_2012)
        results_2008_list = ps1.greedy_election(lost_2008,votes_2008)
        results_sample = [state.get_name() for state in results_sample_list]
        results_2016 = [state.get_name() for state in results_2016_list]
        results_2012 = [state.get_name() for state in results_2012_list]
        results_2008 = [state.get_name() for state in results_2008_list]

        self.assertListEqual(lost_2016,ps1.get_winner_states(ps1.load_election("2016_results.txt")),"Do not modify the list passed in")

        self.assertEqual(set(results_sample), real_sample, "For Sample Results: expected %s, got %s." % (real_sample, list(results_sample)))
        self.assertEqual(set(results_2016), real_2016, "For 2016 Results: expected %s, got %s." % (real_2016, results_2016))
        self.assertEqual(set(results_2012), real_2012, "For 2012 Results: expected %s, got %s." % (real_2012, results_2012))
        self.assertEqual(set(results_2008), real_2008, "For 2008 Results: expected %s, got %s." % (real_2008, results_2008))     

    def test_5_dp_move_max_voters(self):
        real_sample = set([])
        real_2016 = set(['NE', 'WV', 'OK', 'KY', 'TN', 'AL', 'AR', 'MO', 'ND', 'IN', 'LA', 'KS', 'WY', 'SD', 'MS', 'UT', 'SC', 'OH', 'TX', 'ID', 'NC', 'MT', 'IA', 'GA', 'FL', 'AZ', 'AK'])
        real_2012 = set(['NY', 'MA', 'MD', 'DC', 'WA', 'HI', 'VT', 'NJ', 'CA', 'IL', 'CT', 'RI', 'OR', 'MI', 'MN', 'WI', 'NM', 'ME', 'PA', 'IA', 'DE', 'NV', 'CO'])
        real_2008 = set(['DC', 'VT', 'IL', 'NY', 'MA', 'MD', 'MI', 'CA', 'CT', 'WI', 'WA', 'HI', 'OR', 'RI', 'NJ', 'PA', 'NM', 'MN', 'DE', 'NV', 'ME', 'CO'])
        lost_sample = ps1.get_winner_states(ps1.load_election("600_results.txt"))
        lost_2016 = ps1.get_winner_states(ps1.load_election("2016_results.txt"))
        lost_2012 = ps1.get_winner_states(ps1.load_election("2012_results.txt"))
        lost_2008 = ps1.get_winner_states(ps1.load_election("2008_results.txt"))
        votes_reqd_2016 = ps1.ec_votes_reqd(ps1.load_election("2016_results.txt"))
        votes_reqd_2012 = ps1.ec_votes_reqd(ps1.load_election("2012_results.txt"))
        votes_reqd_2008 = ps1.ec_votes_reqd(ps1.load_election("2008_results.txt"))
        lost_votes_2016 = sum(state.get_num_ecvotes() for state in lost_2016)
        lost_votes_2012 = sum(state.get_num_ecvotes() for state in lost_2012)
        lost_votes_2008 = sum(state.get_num_ecvotes() for state in lost_2008)
        results_sample = set(state.get_name() for state in ps1.dp_move_max_voters(lost_sample, 2))            
        results_2016 = [state.get_name() for state in ps1.dp_move_max_voters(lost_2016,lost_votes_2016-votes_reqd_2016)]
        results_2012 = [state.get_name() for state in ps1.dp_move_max_voters(lost_2012,lost_votes_2012-votes_reqd_2012)]
        results_2008 = [state.get_name() for state in ps1.dp_move_max_voters(lost_2008,lost_votes_2008-votes_reqd_2008)]

        self.assertEqual(set(results_sample), real_sample, "For Sample Results: expected States %s, got %s." % (list(real_sample), list(results_sample)))        
        self.assertEqual(set(results_2016), real_2016, "For the 2016 election: expected States %s, got %s." % (list(real_2016), list(results_2016)))
        self.assertEqual(set(results_2012), real_2012, "For the 2012 election: expected States %s, got %s." % (list(real_2012), list(results_2012)))
        self.assertEqual(set(results_2008), real_2008, "For the 2008 election: expected States %s, got %s." % (list(real_2008), list(results_2008)))     

    def test_5_move_min_voters(self):
        real_sample = set(['TX'])
        real_2016 = set(['MI', 'PA', 'WI'])
        real_2012 = set(['FL', 'NH', 'OH', 'VA'])
        real_2008 = set(['FL', 'IN', 'IA', 'NH', 'NC', 'OH', 'VA'])
        lost_sample = ps1.get_winner_states(ps1.load_election("600_results.txt"))
        lost_2016 = ps1.get_winner_states(ps1.load_election("2016_results.txt"))
        lost_2012 = ps1.get_winner_states(ps1.load_election("2012_results.txt"))
        lost_2008 = ps1.get_winner_states(ps1.load_election("2008_results.txt"))
        votes_sample = ps1.ec_votes_reqd(ps1.load_election("600_results.txt"))
        votes_2016 = ps1.ec_votes_reqd(ps1.load_election("2016_results.txt"))
        votes_2012 = ps1.ec_votes_reqd(ps1.load_election("2012_results.txt"))
        votes_2008 = ps1.ec_votes_reqd(ps1.load_election("2008_results.txt"))
        results_sample = set(state.get_name() for state in ps1.move_min_voters(lost_sample, votes_sample))
        results_2016 = set(state.get_name() for state in ps1.move_min_voters(lost_2016,votes_2016))
        results_2012 = set(state.get_name() for state in ps1.move_min_voters(lost_2012,votes_2012))
        results_2008 = set(state.get_name() for state in ps1.move_min_voters(lost_2008,votes_2008))

        self.assertEqual(results_sample, real_sample, "For Sample Results: expected States %s, got %s." % (list(real_sample), list(results_sample)))        
        self.assertEqual(results_2016, real_2016, "For the 2016 election: expected States %s, got %s." % (list(real_2016), list(results_2016)))
        self.assertEqual(results_2012, real_2012, "For the 2012 election: expected States %s, got %s." % (list(real_2012), list(results_2012)))
        self.assertEqual(results_2008, real_2008, "For the 2008 election: expected States %s, got %s." % (list(real_2008), list(results_2008)))     

    def test_6_flip_election(self):
        real_sample = None
        real_2016 = ({('NY', 'MI'): 10705, ('NY', 'WI'): 22749, ('NY', 'PA'): 44293}, 46, 77747)
        real_2012 = ({('UT', 'NH'): 39644, ('UT', 'NV'): 67807, ('UT', 'FL'): 74310, ('UT', 'DE'): 77101, ('UT', 'NM'): 79548, ('UT', 'IA'): 91928, ('UT', 'VT'): 58448, ('AL', 'VT'): 48094, ('AL', 'ME'): 109031, ('AL', 'RI'): 122474}, 64, 768385)
        real_2008 = ({('OK', 'FL'): 236451, ('OK', 'IN'): 28392, ('OK', 'IA'): 146562, ('OK', 'NH'): 46263, ('AL', 'NH'): 22030, ('AL', 'NC'): 14178, ('AL', 'OH'): 262225, ('AL', 'VA'): 154633, ('LA', 'VA'): 79895}, 97, 990629)
        election_sample = ps1.load_election("600_results.txt")
        election_2016 = ps1.load_election("2016_results.txt") 
        election_2012 = ps1.load_election("2012_results.txt") 
        election_2008 = ps1.load_election("2008_results.txt")

        lost_states_sample, ec_needed_sample = ps1.get_winner_states(election_sample), ps1.ec_votes_reqd(election_sample)
        lost_states_2016, ec_needed_2016 = ps1.get_winner_states(election_2016), ps1.ec_votes_reqd(election_2016)
        lost_states_2012, ec_needed_2012 = ps1.get_winner_states(election_2012), ps1.ec_votes_reqd(election_2012)
        lost_states_2008, ec_needed_2008 = ps1.get_winner_states(election_2008), ps1.ec_votes_reqd(election_2008)

        results_sample_g = ps1.flip_election(election_sample, ps1.move_min_voters(lost_states_sample, ec_needed_sample))
        results_2016_g = ps1.flip_election(election_2016, ps1.greedy_election(lost_states_2016, ec_needed_2016))
        results_2012_g = ps1.flip_election(election_2012, ps1.greedy_election(lost_states_2012, ec_needed_2012))

        min_voters_2008 = ps1.move_min_voters(lost_states_2008, ec_needed_2008)
        results_2008_dp = ps1.flip_election(election_2008, min_voters_2008)


        self.assertListEqual(ps1.move_min_voters(lost_states_2008, ec_needed_2008), min_voters_2008,"Do not modify the list passed in")
        
        self.assertTrue(check_valid_mapping(election_sample, results_sample_g, real_sample), "Your flip_election results did not give the correct result. For the sample election you got %s, \n one valid solution is %s." % (results_sample_g, real_sample))
        self.assertTrue(check_valid_mapping(election_2016, results_2016_g, real_2016), "Your flip_election results did not give the correct result. For the 2016 election you got %s, \n one valid solution is %s." % (results_2016_g, real_2016))
        self.assertTrue(check_valid_mapping(election_2012, results_2012_g, real_2012), "Your flip_election results did not give the correct result. For the 2012 election you got %s, \n one valid solution is %s." % (results_2012_g, real_2012,))
        self.assertTrue(check_valid_mapping(election_2008, results_2008_dp, real_2008), "Your flip_election results did not give the correct result. For the 2008 election you got %s, \n one valid solution is %s." % (results_2008_dp, real_2008))


if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestPS1))
    result = unittest.TextTestRunner(verbosity=2).run(suite)
