import mido
import sys

def midi_note_to_frequency(midi_note):
    return 440 * (2 ** ((midi_note - 69) / 12))

def generate_powershell_script(midi_file_path, powershell_script_path):
    mid = mido.MidiFile(midi_file_path)
    
    powershell_code = []
    
    current_time = 0
    grouped_notes = []
    
    for msg in mid.play():
        current_time += msg.time
        if msg.type == 'note_on':
            note_pitch = msg.note
            note_frequency = midi_note_to_frequency(note_pitch)
            grouped_notes.append((note_frequency, current_time))
            print(f"Processed MIDI note {note_pitch} at {current_time:.2f} seconds")
    
    # Create groups with a fixed duration of 2 seconds
    group_duration = 0.4  # seconds
    group_start_time = 0
    group_end_time = group_start_time + group_duration
    
    while group_end_time <= current_time:
        notes_in_group = [note for note in grouped_notes if group_start_time <= note[1] < group_end_time]
        
        if notes_in_group:
            average_frequency = sum(note[0] for note in notes_in_group) / len(notes_in_group)
            powershell_code.append(f'[console]::beep({int(average_frequency)}, {int(group_duration * 1000)})')
        
        group_start_time = group_end_time
        group_end_time += group_duration
    
    with open(powershell_script_path, 'w') as powershell_script:
        powershell_script.write('\n'.join(powershell_code))

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python midi_to_powershell.py input.mid output.ps1")
        sys.exit(1)
    
    input_midi_file = sys.argv[1]
    output_powershell_script = sys.argv[2]
    
    print("Generating PowerShell script...")
    generate_powershell_script(input_midi_file, output_powershell_script)
    print("PowerShell script generated successfully!")
