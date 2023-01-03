import json 

'''
    An implementation of the Needleman-Wunsch algorithm (https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm)
    Based on https://wilkelab.org/classes/SDS348/2019_spring/labs/lab13-solution.html
'''

class Needleman_Wunsch:
    def __init__(self):
        self.gap_penalty = -1
        self.match_award = 1
        self.mismatch_penalty = -1
        self.insertion_character = "▁"

    def print_matrix(self, mat):
        # a helper function to print out matrices
        # Loop over all rows
        for i in range(0, len(mat)):
            print("[", end = "")
            # Loop over each column in row i
            for j in range(0, len(mat[i])):
                # Print out the value in row i, column j
                print(mat[i][j], end = "")
                # Only add a tab if we're not in the last column
                if j != len(mat[i]) - 1:
                    print("\t", end = "")
            print("]\n")

    def zeros(self, rows, cols):
        # A function for making a matrix of zeroes
        retval = []
        # Set up the rows of the matrix
        for x in range(rows):
            # For each row, add an empty list
            retval.append([])
            # Set up the columns in each row
            for y in range(cols):
                # Add a zero to each column in each row
                retval[-1].append(0)
        # Return the matrix of zeros
        return retval

    def match_score(self, alpha, beta):
        # A function for determining the score between any two bases in alignment
        if alpha == beta:
            return self.match_award
        elif alpha == self.insertion_character or beta == self.insertion_character:
            return self.gap_penalty
        else:
            return self.mismatch_penalty

    def needleman_wunsch(self, seq1, seq2):
        # The function that actually fills out a matrix of scores
        # Store length of two sequences
        n = len(seq1)  
        m = len(seq2)
        
        # Generate matrix of zeros to store scores
        score = self.zeros(m+1, n+1)
       
        # Calculate score table
        
        # Fill out first column
        for i in range(0, m + 1):
            score[i][0] = self.gap_penalty * i
        
        # Fill out first row
        for j in range(0, n + 1):
            score[0][j] = self.gap_penalty * j
        
        # Fill out all other values in the score matrix
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                # Calculate the score by checking the top, left, and diagonal cells
                match = score[i - 1][j - 1] + self.match_score(seq1[j-1], seq2[i-1])
                delete = score[i - 1][j] + self.gap_penalty
                insert = score[i][j - 1] + self.gap_penalty
                # Record the maximum score from the three possible scores calculated above
                score[i][j] = max(match, delete, insert)
        
        # Traceback and compute the alignment 
        # Create variables to store alignment
        align1 = ""
        align2 = ""
        
        # Start from the bottom right cell in matrix
        i = m
        j = n
        
        # We'll use i and j to keep track of where we are in the matrix, just like above
        while i > 0 and j > 0: # end touching the top or the left edge
            score_current = score[i][j]
            score_diagonal = score[i-1][j-1]
            score_up = score[i][j-1]
            score_left = score[i-1][j]
            
            # Check to figure out which cell the current score was calculated from,
            # then update i and j to correspond to that cell.
            if score_current == score_diagonal + self.match_score(seq1[j-1], seq2[i-1]):
                align1 += seq1[j-1]
                align2 += seq2[i-1]
                i -= 1
                j -= 1
            elif score_current == score_up + self.gap_penalty:
                align1 += seq1[j-1]
                align2 += self.insertion_character
                j -= 1
            elif score_current == score_left + self.gap_penalty:
                align1 += self.insertion_character
                align2 += seq2[i-1]
                i -= 1

        # Finish tracing up to the top left cell
        while j > 0:
            align1 += seq1[j-1]
            align2 += self.insertion_character
            j -= 1
        while i > 0:
            align1 += self.insertion_character
            align2 += seq2[i-1]
            i -= 1
        
        # Since we traversed the score matrix from the bottom right, our two sequences will be reversed.
        # These two lines reverse the order of the characters in each sequence.
        align1 = align1[::-1]
        align2 = align2[::-1]
        
        return (align1, align2)

    def create_character_matrix(self, source, target):
        '''
            Given two lists of aligned texts in the source and target languages, create the character alignment matrix (CAT)
        '''
        CAM = dict()
        for s, t in zip(source, target):
            output_1, output_2 = self.needleman_wunsch(s, t)
            #self.print_matrix(self.needleman_wunsch(s, t))
            for i in range(len(output_1)):
                if output_1[i] not in CAM:
                    CAM[output_1[i]] = dict()

                if output_2[i] not in CAM[output_1[i]]:
                    CAM[output_1[i]][output_2[i]] = 0

                CAM[output_1[i]][output_2[i]] += 1

        return CAM # character alignment matrix

