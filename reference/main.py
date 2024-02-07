import sys
from modules.generate_midi_from_chord import *
from modules.chord_map import *
import openai
import os
from dotenv import load_dotenv



def generate_chord_progression(prompt):
    try:
        # Ensure API key is set in your environment variables
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        if not openai.api_key:
            raise ValueError("OpenAI API key is not set in environment variables.")

        # few-shot prompt
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional musician and music theorist. Your job is to create a good 8-bar chord progression in C, suited to the genre. Only provide the strings as shown in the examples. Be creative, but not too odd. Take care of musical qualities. Don't always start with C; don't overly use 2-5-1. Do not use the character ø; replace it with b5 notation. DO NOT OUTPUT ANYTHING BUT 8 BARS OF CHORD SYMBOLS."},
                {"role": "user", "content": "give me a jazz chord progression"},
                {"role": "assistant", "content": "FM7 | Em7 A7b9 | Dm7 G7 | CM7 | F#m7b5 B7 | Em7 | A9 D7 | G7 | C#dim7"},
                {"role": "user", "content": "give me a jazz chord progression"},
                {"role": "assistant", "content": ""},
                {"role": "user", "content": prompt}
            ],
            temperature = 0.8  # experiment with the value; smaller to get less random results
        )
        # print("response: " + response.choices[0].message['content'])
        return response.choices[0].message['content']
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    
    

def format_symbols(chord_symbols_raw):
    '''
    given a string of chord progression, format it so I can process it later more smoothly.
    For example, a given string can look like "Am7 | D7 | GM7 | CM7 | Bm7b5 | E7 | Am7 | Dm7 G7", 
    where each chunk separated by | | represents a musical bar. 
    In the above example, bar 4 is CM7, and bar 8 is Dm7 followed by G7. 
    This function formats this into "Am7 D7 GM7 CM7 Bm7b5 E7 Am7 Dm7/G7". 
    Gets rid of the | marks, and connects the chords within the same bar with /s.
    '''
    # checking the input
    print("raw: ")
    print("  " + chord_symbols_raw)
    
    # if the last letter is |, delete it
    if chord_symbols_raw[-1] == "|":
        chord_symbols_raw = chord_symbols_raw[:-1]
    bars = chord_symbols_raw.split(" | ")
    
    # formatting logic
    for i in range(len(bars)):
        if " " in bars[i]:
            bars[i] = bars[i].replace(" ", "/")
    formatted_progression = " ".join(bars)
    formatted_progression.replace('.', '').replace(',', '')
    
    # if the last letter is /, delete it
    if formatted_progression[-1] == "/":
        formatted_progression = formatted_progression[:-1]
    
    # checking the output
    print("formatted: ")
    print("  " + formatted_progression)
    
    return formatted_progression


def main():

    # Load environment variables from .env file
    load_dotenv()
    
    prompt = "Generate a jazz chord progression"
    chord_symbols_raw = generate_chord_progression(prompt)
    chord_symbols = format_symbols(chord_symbols_raw)
    
    mode = 1 # 0 is normal, 1 is with more bass
    
    # Check if the result folder exists, if not, create it
    result_folder = "./result"
    if not os.path.exists(result_folder):
        os.makedirs(result_folder)
    
    music_stream, chord_name = generate_midi_from_chord(chord_symbols, mode)
    filename = f"{result_folder}/{chord_name}.mid"  # Construct the filename using f-string
    mf = midi.translate.streamToMidiFile(music_stream)
    mf.open(filename, 'wb')
    mf.write()
    mf.close()
    
    # drum_pattern = drum_pattern()
    # merge_midi_files(drum_pattern, filename, 'merged_midi.mid')
        
        
        
        
if __name__ == "__main__":
    main()

