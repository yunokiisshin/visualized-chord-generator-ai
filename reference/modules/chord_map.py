'''
chord_map computes the generation for a given bar.
'''

from music21 import *
from music21.pitch import Pitch
import random


# dictionary container for every possible note for the processed chord; refreshes per chord
# contains ints that represent MIDI note value
note_dict = dict([("root", []), ("third", []), ("fifth", []), ("seventh", []), ("ninth", []), ("extentions", [])])

# Constants for MIDI note range
LOWEST_NOTE = pitch.Pitch("F#3").midi
HIGHEST_NOTE = pitch.Pitch("D5").midi


def shift(note, semitones):
    ''' Shifts a note by a given number of semitones. '''
    return Pitch(note.midi + semitones)


def fill_dict_value(note_dict, key, note):
    ''' Fills up the note_dict with MIDI note values for a given pitch range. '''
    note_val = pitch.Pitch(note)
    while note_val.midi >= LOWEST_NOTE:
        note_val.midi -= 12
    note_val.midi += 12
    while note_val.midi <= HIGHEST_NOTE:
        note_dict[key].append(note_val.midi)
        note_val.midi += 12
        

'''fills up the entire note_dict'''
def prepare_note_dict(root_note, chord_type):
    
    root = Pitch(root_note)

    if chord_type == '': # major triad
        third = shift(root, 4)
        fifth = shift(root, 7)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
    
    elif chord_type == 'm': # minor triad
        third = shift(root, 3)
        fifth = shift(root, 7)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
    
    elif chord_type == '7': # dominant 7th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        fill_dict_value(note_dict, "seventh", seventh)
    
    elif chord_type == 'M7' or 'Maj7': # major 7th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 11)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        
    elif chord_type == 'm7': # minor 7th
        third = shift(root, 3)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
   
    elif chord_type == 'dim7': # dimished 7th
        third = shift(root, 3)
        fifth = shift(root, 6)
        seventh = shift(root, 9)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        
    elif chord_type == 'M9': # major 9th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 11)
        ninth = shift(root, 14)
        fill_dict_value(note_dict, "ninth", ninth)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        
    elif chord_type == 'm9': # minor 9th
        third = shift(root, 3)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        ninth = shift(root, 14)
        fill_dict_value(note_dict, "ninth", ninth)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
    
    elif chord_type == '9': # dominant 9th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        ninth = shift(root, 14)
        fill_dict_value(note_dict, "ninth", ninth)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        
    elif chord_type == '7b9': # dominant 7th flat 9th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        ninth = shift(root, 13)
        fill_dict_value(note_dict, "ninth", ninth)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
    
    elif chord_type == '7#9': # dominant 7th sharp 9th
        third = shift(root, 4)
        fifth = shift(root, 7)
        seventh = shift(root, 10)
        ninth = shift(root, 15)
        fill_dict_value(note_dict, "ninth", ninth)
        fill_dict_value(note_dict, "seventh", seventh)
        fill_dict_value(note_dict, "root", root)
        fill_dict_value(note_dict, "third", third)
        fill_dict_value(note_dict, "fifth", fifth)
        
    else: # throw error
        error = "Chord type not recognized."
        raise ValueError(error)
        
        
    
    if 'sus4' in chord_type: # alter the 3rd in the chord up a step
        third = shift(root, 5)
        note_dict["third"].clear()
        fill_dict_value(note_dict, "third", third)
        
    if 'sus2' in chord_type: # alter the 3rd in the chord down a step
        third = shift(root, 2)
        note_dict["third"].clear()
        fill_dict_value(note_dict, "third", third)
        
    if 'b5' in chord_type: # alter the 5th in the chord down a step
        note_dict["fifth"].clear()
        fifth = shift(root, 6)
        fill_dict_value(note_dict, "fifth", fifth)
    
    if '#5' in chord_type: # alter the 5th in the chord up a step
        note_dict["fifth"].clear()
        fifth = shift(root, 8)
        fill_dict_value(note_dict, "fifth", fifth)
        
        
    
'''generate the current chord based on the previous input'''
def generate(root_note, chord_type, mode, previous_notes): # previous notes is list of pitch objects
    
    if mode == 0:  # each chordal note is only added once; basically 3 or 4 notes
        # convert previous_notes to int list
        previous_val = []
        for note in previous_notes:
            previous_val.append(note.midi)
        previous_val = sorted(previous_val)

        # clear the chord dictionary
        for key in note_dict.keys():
            note_dict[key].clear()
            
        prepare_note_dict(root_note, chord_type)  
        
        # notes have to be a list of Pitch object
        notes = []
        
        # if this is the first time generating a chord
        if previous_val == []:
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            
            first_note = random.choice(note_list)
            notes.append(first_note)
            
            # choose the rest of the notes
            if first_note in note_dict["root"]: # choosing third and fifth
                bucket = [] # temporary container
                
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)

        else:   # there is a previous chord generated
            
            # finding the middle note from previous chord as reference
            ref = previous_val[len(previous_val)//2]
        
            # create a list of all notes
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            closest = note_list[0]
            distance = 100
            for i, note in enumerate(note_list):
                if abs(ref - note) < distance:
                    closest = note_list[i]
                    distance = abs(closest-ref)

            # make that note the first note of the current chord
            first_note = closest
            notes.append(first_note)
            
            if first_note in note_dict["root"]: 
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)        
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
        
        # convert the value to MIDI-suited data
        note_pitches = []  
                
        for note in notes:
            midi_number = note
            p = pitch.Pitch()
            p.midi = midi_number
            note_pitches.append(p)
        
        return note_pitches
    
    
    elif mode == 1:  # 4 or 5-note composition
        # convert previous_notes to int list
        previous_val = []
        for note in previous_notes:
            previous_val.append(note.midi)
        previous_val = sorted(previous_val)

        # clear the chord dictionary
        for key in note_dict.keys():
            note_dict[key].clear()
        
        prepare_note_dict(root_note, chord_type)   
        
        # notes have to be a list of Pitch object
        notes = []
        
        # if this is the first time generating a chord
        if previous_val == []:
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            
            first_note = random.choice(note_list)
            notes.append(first_note)
            
            if first_note in note_dict["root"]: # choosing third and fifth
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]:
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: 
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                    
            bottom_root = note_dict["root"][0]
            if bottom_root in notes:
                notes.append(bottom_root-12)
            else:
                notes.append(bottom_root)
                

        else:   # there is a previous chord generated
            
            # finding the middle note from previous chord as reference
            ref = previous_val[len(previous_val)//2]
        
            # create a list of all notes
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            closest = note_list[0]
            distance = 100
            
            for i, note in enumerate(note_list):
                if abs(ref - note) < distance:
                    closest = note_list[i]
                    distance = abs(closest-ref)

            # make that note the first note of the current chord
            first_note = closest
            notes.append(first_note)
            
            if first_note in note_dict["root"]: 
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)        
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
            
            elif first_note in note_dict["seventh"]: 
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
            
            bottom_root = note_dict['root'][0]
            if bottom_root not in notes:
                notes.append(bottom_root)
                
            else:
                notes.append(bottom_root-12)
                
        note_pitches = []  
                
        for note in notes:
            midi_number = note
            p = pitch.Pitch()
            p.midi = midi_number
            note_pitches.append(p)
        
        return note_pitches
    
    elif mode == 2: # 5 or 6-note generation
        # convert previous_notes to int list
        previous_val = []
        for note in previous_notes:
            previous_val.append(note.midi)
        previous_val = sorted(previous_val)

        # clear the chord dictionary
        for key in note_dict.keys():
            note_dict[key].clear()
        
        
        # notes have to be a list of Pitch object
        notes = []
        
        # if this is the first time generating a chord
        if previous_val == []:
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            
            first_note = random.choice(note_list)
            notes.append(first_note)
            
            if first_note in note_dict["root"]: # choosing third and fifth
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]:
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: 
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)

            bottom_root = note_dict['root'][0]
            
            if bottom_root in notes:
                notes.append(bottom_root-12)
                notes.append(bottom_root-24)
                        
            else:         
                notes.append(bottom_root-12)
                notes.append(bottom_root)
            

        else:   # there is a previous chord generated
            
            # finding the middle note from previous chord as reference
            ref = previous_val[len(previous_val)//2]
        
            # create a list of all notes
            note_list = []
            for value in note_dict.values():
                for item in value:
                    note_list.append(item)
            closest = note_list[0]
            distance = 100
            
            for i, note in enumerate(note_list):
                if abs(ref - note) < distance:
                    closest = note_list[i]
                    distance = abs(closest-ref)

            # make that note the first note of the current chord
            first_note = closest
            notes.append(first_note)
            
            if first_note in note_dict["root"]: 
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                bucket = []
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)        
                
                bucket.clear()
                for item in note_dict["seventh"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
            
            elif first_note in note_dict["seventh"]: 
                bucket = []
                for item in note_dict["third"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                second_note = random.choice(bucket)
                notes.append(second_note)
                
                bucket.clear()
                for item in note_dict["fifth"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                third_note = random.choice(bucket)
                notes.append(third_note)
                
                bucket.clear()
                for item in note_dict["root"]:
                    if abs(item-first_note) <= 9:
                        bucket.append(item)
                if bucket != []:
                    fourth_note = random.choice(bucket)
                    notes.append(fourth_note)
                    
                bucket.clear()
            
            bottom_root = note_dict['root'][0]
            
            if bottom_root in notes:
                notes.append(bottom_root-12)
                notes.append(bottom_root-24)
                        
            else:         
                notes.append(bottom_root-12)
                notes.append(bottom_root)
            
                
                
        note_pitches = []  
                
        for note in notes:
            midi_number = note
            p = pitch.Pitch()
            p.midi = midi_number
            note_pitches.append(p)
        
        return note_pitches