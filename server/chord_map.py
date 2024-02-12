'''
chord_map computes the generation for a given bar.
'''

from music21 import *
from music21.pitch import Pitch
import random


# handy class to control json_output element (also a class practice)
class jsonElement:
    
    def __init__(self, chord=str, length=int, notes=list): 
        self.content = {
            "chord": chord,
            "length": length,
            "notes": notes
        }

    def setChord(self, chord):
        self.content["chord"] = chord        

    def setLength(self, length):
        self.content["length"] = length        

    def setNotes(self, notes):
        self.content["notes"] = notes
        
    def returnContent(self):
        return self.content

    def printContent(self):
        print("content: ")
        print(self.content["chord"])
        print(self.content["length"])
        print(self.content["notes"])


# dictionary container for every possible note for the processed chord; refreshes per chord
# contains ints that represent MIDI note value
note_dict = dict([("root", []), ("third", []), ("fifth", []), ("seventh", []), ("ninth", []), ("extentions", [])])

# Constants for MIDI note range
LOWEST_NOTE = pitch.Pitch("F3").midi
HIGHEST_NOTE = pitch.Pitch("E5").midi
# print("LOWEST_NOTE: ", LOWEST_NOTE) # 53
# print("HIGHEST_NOTE: ", HIGHEST_NOTE) # 76

''' Shifts a note by a given number of semitones. '''
def shift(note, semitones):
    return Pitch(note.midi + semitones)


''' Fills up the note_dict with MIDI note values for a given pitch range. '''
def fill_dict_value(note_dict, key, note):
    note_val = pitch.Pitch(note)
    while note_val.midi >= LOWEST_NOTE:
        note_val.midi -= 12
    note_val.midi += 12
    while note_val.midi <= HIGHEST_NOTE:
        note_dict[key].append(note_val.midi)
        note_val.midi += 12
        

'''returns a list of intervals for fill_dict_value to process'''
def prepare_note_dict(root_note, chord_type):
    
    root = Pitch(root_note)
    
    is_sus4, is_sus2, is_b5, is_sharp5, is_b9, is_sharp9 = False, False, False, False, False, False
    # Remove any suffixes from the chord type, it would be processed later
    if 'sus4' in chord_type:
        chord_type = chord_type.replace('sus4', '')
        is_sus4 = True
    
    if 'sus2' in chord_type:
        chord_type = chord_type.replace('sus2', '')
        is_sus2 = True
    
    if 'b5' in chord_type:
        chord_type = chord_type.replace('b5', '')
        is_b5 = True
        
    if '#5' in chord_type:
        chord_type = chord_type.replace('#5', '')
        is_sharp5 = True
        
    if 'b9' in chord_type:
        chord_type = chord_type.replace('b9', '')
        is_b9 = True
        
    if '#9' in chord_type:
        chord_type = chord_type.replace('#9', '')
        is_sharp9 = True
        
    # chord_formulas contain intervals for possible chord types
    chord_formulas = {
        '': [0, 4, 7],  # Major triad
        'm': [0, 3, 7],  # Minor triad
        '7': [0, 4, 7, 10],  # Dominant 7th
        'M7': [0, 4, 7, 11],  # Major 7th
        'Maj7': [0, 4, 7, 11],  
        'maj7': [0, 4, 7, 11],  
        'm6': [0, 3, 7, 9],  # Minor 6th
        'm7': [0, 3, 7, 10],  # Minor 7th
        'dim7': [0, 3, 6, 9],  # Diminished 7th
        'M9': [0, 4, 7, 11, 2],  # Major 9th
        'm9': [0, 3, 7, 10, 2],  # Minor 9th
        '9': [0, 4, 7, 10, 2],  # Dominant 9th
        '13': [0, 4, 7, 10, 2, 9],  # Dominant 13th
        '7#11': [0, 4, 7, 10, 6],  # Dominant 7th sharp 11th
        '7b13': [0, 4, 7, 10, 9],  # Dominant 7th flat 13th
    }
    
    if chord_type not in chord_formulas.keys():
        error = "Chord type not recognized."
        raise ValueError(error)
    
    # interval_list: list of intervals to be added to the root note
    interval_list = chord_formulas[chord_type]
    
    interval_strings = ["root", "third", "fifth", "seventh", "ninth", "extentions"]
    
    for i, interval in enumerate(interval_list):
        interval_string = str(interval_strings[i])  # Ensure this results in a string
        note = shift(root, interval)
        fill_dict_value(note_dict, interval_string, note)
        

    # Alter the notes based on the chord type
    if is_sus4: 
        note_dict["third"].clear()
        third = shift(root, 5)
        fill_dict_value(note_dict, "third", third)
        
    if is_sus2: 
        note_dict["third"].clear()
        third = shift(root, 2)
        fill_dict_value(note_dict, "third", third)
        
    if is_b5: 
        note_dict["fifth"].clear()
        fifth = shift(root, 6)
        fill_dict_value(note_dict, "fifth", fifth)
    
    if is_sharp5: 
        note_dict["fifth"].clear()
        fifth = shift(root, 8)
        fill_dict_value(note_dict, "fifth", fifth)
        
    if is_b9:
        note_dict["ninth"].clear()
        ninth = shift(root, 1)
        fill_dict_value(note_dict, "ninth", ninth)
        if len(note_dict["ninth"]) > 1:
            note_dict["ninth"].pop(0)
        
    if is_sharp9:
        note_dict["ninth"].clear()
        ninth = shift(root, 3)
        fill_dict_value(note_dict, "ninth", ninth)
        if len(note_dict["ninth"]) > 1:
            note_dict["ninth"].pop(0)
        
    # print("note_dict: ", note_dict)
        
        
    
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
            if first_note in note_dict["root"]: 
                 # temporary container
                keys = ["third", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                
                keys = ["root", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                
                keys = ["root", "third", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["seventh"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["ninth"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)

            elif first_note in note_dict["extentions"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "ninth"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
            
            else: 
                raise ValueError("Error: you're not supposed to see this")

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
            
            # choose the rest of the notes
            if first_note in note_dict["root"]: 
                 # temporary container
                keys = ["third", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                
                keys = ["root", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                
                keys = ["root", "third", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["seventh"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["ninth"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)

            elif first_note in note_dict["extentions"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "ninth"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
            
            else: 
                raise ValueError("Error: you're not supposed to see this")
            
    
    else:          # mode == 1; 4 or 5-note composition
        
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
            if first_note in note_dict["root"]: 
                 # temporary container
                keys = ["third", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                
                keys = ["root", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                
                keys = ["root", "third", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["seventh"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["ninth"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)

            elif first_note in note_dict["extentions"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "ninth"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
            
            else: 
                raise ValueError("Error: you're not supposed to see this")
            
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
            
            # choose the rest of the notes
            if first_note in note_dict["root"]: 
                 # temporary container
                keys = ["third", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
                
            elif first_note in note_dict["third"]: # choosing root and fifth
                
                keys = ["root", "fifth", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                
            elif first_note in note_dict["fifth"]: # choosing root and third
                
                keys = ["root", "third", "seventh", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["seventh"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "ninth", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
                    
            elif first_note in note_dict["ninth"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "extentions"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)

            elif first_note in note_dict["extentions"]: # choosing root and third
                
                keys = ["root", "third", "fifth", "seventh", "ninth"]
                random.shuffle(keys)
                for key in keys:
                    values = note_dict[key]
                    if values:  # Proceed only if there are values
                        # Filter values based on the condition, use min to ensure at least one element is chosen
                        valid_values = [value for value in values if abs(value - first_note) <= 9 or len(values) == 1]
                        next_note = random.choice(valid_values)  # Choose a random valid value
                        notes.append(next_note)
            
            else: 
                raise ValueError("Error: you're not supposed to see this")
            
            
            bottom_root = note_dict['root'][0]
            if bottom_root in notes:
                notes.append(bottom_root-12)
                
            else:
                notes.append(bottom_root)
    
    # print("Final notes: " + str(notes))
    
    jsonResult = jsonElement(str(root_note + chord_type), 4, notes)
    
    # convert the value to MIDI-suited data            
    note_pitches = []  
            
    for note in notes:
        midi_number = note
        p = pitch.Pitch()
        p.midi = midi_number
        note_pitches.append(p)
    
    return note_pitches, notes, jsonResult