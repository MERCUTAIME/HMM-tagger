# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys
from collections import defaultdict

def tag(training_list, test_file, output_file):
    # Tag the words from the untagged input file and write them into the output file.
    # Doesn't do much else beyond that yet.
    print("Tagging the file.")
    #
    # YOUR IMPLEMENTATION GOES HERE
    #
    tag_count = defaultdict(int)
    words = []
    transition_count = defaultdict(int)
    emission_count = defaultdict(int)
    prev = 'PUN'
    tag_count[prev] +=1

    # import training file and record
    for f in training_list:
        file = open(f)
        # print(file)
        for line in file.readlines():
            word = line.split(' : ')[0]
            tag = line.split(' : ')[1].split('\n')[0]
            tag_count[tag]+=1
            if word not in words:
                words.append(word)
            transition_count[(prev, tag)]+=1
            emission_count[(word, tag)] += 1     
            prev = tag
            
    # print('tag_count')
    # print(tag_count)
    # print('transition_count')
    # print(transition_count)
    # print('emission_count')
    # print(emission_count)
    
    #open test file
    testfile = open(test_file)
    test_word = []
    # print(testfile)
    for line in testfile.readlines():
        test_word.append(line.split('\n')[0])
        
    #open output file
    outputfile = open(output_file, "w")
    
    
    #initial probs table init_probs[i] = probs pof tags[i]
    tags = list(tag_count.keys())
    init_probs = [0 for i in range(len(tags))]
    
    for i in range(len(tags)):
        init_probs[i] = tag_count[tags[i]]/ sum(tag_count.values())
    
    #print(init_probs)
    
    #transition probs table trans_probs[i][j] = probs of going from tags[i] to tags[j]   
    trans_probs = [[0 for i in range(len(tags))] for j in range(len(tags))]
    
    for i in range(len(tags)):
        for j in range(len(tags)):
            pair_count = 0
            curr_pair = (tags[i],tags[j])
            if curr_pair in transition_count:
                pair_count = transition_count[curr_pair]
                
            prev_tag_count = tag_count[tags[i]]
            trans_probs[i][j] = pair_count/ prev_tag_count
            
    # print(trans_probs)
    
    #emission probs table emi_probs[i][j] = probs of word i to be tagged with tag j
    emi_probs = [[0 for i in range(len(tags))] for j in range(len(words))]
    
    for i in range(len(words)):
        for j in range(len(tags)):
            tagged_word_count = 0
            curr_word_tag = (words[i],tags[j])
            
            if curr_word_tag in emission_count:
                tagged_word_count = emission_count[curr_word_tag]
                
            t_count = tag_count[tags[j]]
            emi_probs[i][j] = tagged_word_count/ t_count
    
    # print(emi_probs)
    
    #HMM Tagger with Viterbi algorithm
    result = []
    prev_tag = ''
    for i in range(len(test_word)):
        p = []
        
        for j in range(len(tags)):

            emi_p = 1
            if test_word[i] in words:
                emi_p = emi_probs[words.index(test_word[i])][j]
                
            if i == 0:
                state_p = emi_p * init_probs[j]
            else:
                trans_p = trans_probs[tags.index(prev_tag)][j]
                state_p = emi_p * trans_p
            p.append(state_p)

        best_prob = max(p)

        state = tags[p.index(best_prob)]

        prev_tag = state

        # result.append((test_word[i], state))
        outputfile.write(test_word[i])
        outputfile.write(" : ")
        outputfile.write(state)
        outputfile.write("\n")
    # print(result)
    file.close()
    testfile.close()
    outputfile.close()
      

if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag (training_list, test_file, output_file)