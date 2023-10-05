#event_coref

To run the code, make sure the input file is at the local folder and do -python main.py [input_file_name] [output_file_name]

The module require TRIPS and numpy. We use TRIPS to handle the ontology and numpy to solve agreement constraint by some dot products. 

Abstract 
	In this module we treat the objective as a constraint satisfaction problem with certain preferences. 

	The constraints involve: 
		1) number/gender agreemen
		2) semantic agreement considering person-pronoun (e.g. he, she, they) and non-person pronoun (e.g. it), 
		3) proper noun agreement (two NAME-type objects are identical only if they have the exact name)
		4) non-reflexive agreement (i.e. unless a reflexive pronoun is used, entities in the same sentence should not refer to each other)
		5) event-coref constraint (only pronoun 'it' has the potential to refer to an event, represented by verb token)

	The preferences we implemented in this module are mainly recency and discourse_center, which are expressed by the ordered domain of variables. We took the assumption that the inputs were updated incrementally and a new input should not interfere with the co-reference that has been already assigned. Given that, we approached the overall optimal result by adding up the locally optimal fragments, such that each input would take the optimal assignment only with respect to its local context and has no power to alter the assignment or the discourse center that have been already determined. The non-interfering assumption simplified our model quite a bit yet still achieving 100% accuracy on given samples. 


General Code Structure:

	The module would first tokenize the discourse entities with the input format as [SPEC] [STRING] [ONTOLOGY] [ID], and initiate a SOLUTION class that has: 
	1) list of input sequences 
	2) a mapping (dict) of variables to potential corefs 
	3) a domain of variables of our interest. 
	In general, the model tries to modify the mappings and domain with respect to the constraints, and return the first solution with the CSP algorithm. This will be the optimal solution under our non-interfering assumption. 


	The py files and their functions are summarized below:
	main.py				Preprocessing and output sequence
	domain_modification.py		Trimming the domain of variables and determining the variable of interest
	evidence.py 			Initially set up to try implementing non-deterministic method like wu-palmer score. End up being used only for plurality check. 
	entailings.py			For semantic agreement 
	CSP.py 				Major assignment algorithm. 

Strength and weakness:
	While this module could effectively solve the 6 given examples, the non-interfering assumption we take is actually very dangerous. This is especially the case considering discourse center. In fact, in the examples provided, it is usually the agreement features that helps the algorithm most, by trimming off most of the potential assignments and passing very few choices to the CSP algorithm for recency / discourse center check. One could easily make up examples where the best assignment won't exactly follow the order as suggested in the reading (in fact, the reading itself admits the correct order is still debated). 
	Furthermore, the module currently has no way to handle the distributive/collective referent efficiently under conjunction, especially when two sub-fragments are both in plural form (e.g. the engineers and the boys). In fact, whether a plural pronoun "they" refer to one or the whole would largely depend on the semantic context, which the TRIPS ontology alone won't be able to capture. We default our algorithms to distributively map the assignment, unless a collective read is the only possible way. 
	In general, the should be a descent toy module to deterministically assigning the co-references based on the constraint, while it would be not much effective when an inference based on pure semantic context must come into play.


